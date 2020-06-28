from flask import Flask, jsonify, request, session, render_template, make_response
import services.verification as vf
import jwt
import json
import datetime
from routes import app
from config import SECRET
from services.auth import check_for_token
from bson import json_util, ObjectId
from services import db

@app.route('/api/v1/login', methods=['GET', 'POST'])
def login():
    if request.headers['Content-Type'] == 'application/json':
            rq = json.loads(request.data)
            if set(rq.keys()) == {'email', 'password'}:
                if vf.verify_password(rq):
                    # session['logged_in'] = True
                    token = jwt.encode({
                        'user': rq['email'],
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=6),
                        'id': str(db.accounts.find_one({"email": rq['email']})['_id']),
                    },
                    SECRET)
                    return jsonify({'token': token.decode('utf-8')})
                else:
                    return make_response('User or password wrong', 403, {'WWW-Authenticate': 'Basic realm="Login required"'})
            return jsonify({'message': 'Good form required'}), 406
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422


@app.route('/api/v1/register', methods=['POST'])
def register():
    if request.headers['Content-Type'] == 'application/json':
            status = vf.account_check(json.loads(request.data))
            if status== 406:
                return jsonify({'message': 'Good form required'}), 406
            if status == 409:
                return jsonify({'message': 'Email already exist'}), 409

            return jsonify({'message': 'account has been added'}), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422


@app.route('/api/v1/account', methods=['GET'])
@check_for_token
def getAllAccount():
    req = vf.get_all_account()
    if req == 404:
        return jsonify({'message': 'the database is empty'}), 404
    return json_util.dumps(req), 200

@app.route('/api/v1/account/<account_id>', methods=['GET'])
@check_for_token
def getAccount(account_id):
    req = vf.get_account(account_id)
    if req == 409:
        return jsonify({'message': 'account_id not found'}), 409
    return json_util.dumps(req), 200


@app.route('/api/v1/account/<account_id>/user/<user_id>', methods=['GET'])
@check_for_token
def getUser(account_id, user_id):
    req = vf.get_user(user_id)
    if req == 409:
        return jsonify({'message': 'user_id not found'}), 409
    return json_util.dumps(req), 200

@app.route('/api/v1/account/<account_id>/user', methods=['POST'])
@check_for_token
def addUser(account_id):
    if request.headers['Content-Type'] == 'application/json':
            status = vf.add_user(account_id, json.loads(request.data))
            if status== 409:
                return jsonify({'message': 'account id not found'}), 406

            return jsonify({'message': 'user has been added', 'data' : json_util.dumps(status)}), 200
    else:
        print('cass toi')
        return jsonify({'error': 'Please use application/json as content type'}), 422

@app.route('/api/v1/account/<account_id>/user/<user_id>', methods=['PUT', 'PATCH'])
@check_for_token
def updateUser(account_id, user_id):
    if request.headers['Content-Type'] == 'application/json':
        req = vf.update_user(user_id, json.loads(request.data))
        if req == 409:
            return jsonify({'message': 'user_id not found'}), 409
        return jsonify({'message': 'user has been updated'}), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422

@app.route('/api/v1/account/<account_id>/user/<user_id>', methods=['DELETE'])
@check_for_token
def deleteUser(account_id, user_id):
        status = vf.remove_user(account_id, user_id)
        if status== 409:
            return jsonify({'message': 'account id not found'}), 406

        return jsonify({'message': 'user has been deleted'}), 200


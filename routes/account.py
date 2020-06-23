from flask import Flask, jsonify, request, session, render_template, make_response
import services.verification as vf
import jwt
import json
import datetime
from routes import app

@app.route('/api/v1/login', methods=['GET', 'POST'])
def login():
    print(request.headers)
    if request.headers['Content-Type'] == 'application/json':
            rq = json.loads(request.data)
            if set(rq.keys()) == {'email', 'password'}:
                if vf.verify_password(rq):
                    session['logged_in'] = True
                    token = jwt.encode({
                        'user': rq['email'],
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                    },
                    app.config['SECRET_KEY'])
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

            return jsonify({'message': 'account added to the database'}), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422

@app.route('/api/v1/<account_id>/user', methods=['POST'])
def addUser(account_id):
    if request.headers['Content-Type'] == 'application/json':
            status = vf.add_user(account_id, json.loads(request.data))
            if status== 409:
                return jsonify({'message': 'account id not found'}), 406

            return jsonify({'message': 'user added to the account'}), 200
    else:
        return jsonify({'error': 'Please use application/json as content type'}), 422

@app.route('/api/v1/<account_id>/user/<user_id>', methods=['DELETE'])
def deleteUser(account_id, user_id):
        status = vf.remove_user(account_id, user_id)
        if status== 409:
            return jsonify({'message': 'account id not found'}), 406

        return jsonify({'message': 'user has been deleted'}), 200

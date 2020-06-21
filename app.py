from flask import Flask, jsonify, request, session, render_template, make_response
from functools import wraps
import jwt
import datetime
import services.verification as vf
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['SECRET_KEY'] = 'Fluance'

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers['Authorization'].replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped

@app.route('/')
def index():
    print(request.headers['Authorization'].replace('Bearer ', ''))
    return ''
    # return 'hi, for now we use /login and /register only'

@app.route('/login', methods=['GET', 'POST'])
def login():
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

@app.route('/register', methods=['POST'])
def register():
    if request.headers['Content-Type'] == 'application/json':
        status = vf.account_check(json.loads(request.data))
        if status== 406:
            return jsonify({'message': 'Good form required'}), 406
        if status == 409:
            return jsonify({'message': 'Email already exist'}), 409

        return jsonify({'message': 'account added to the database'}), 200

@app.route('/auth')
@check_for_token
def authorised():
    """
    This page has been created to test the token only
    :return:
    """
    return 'page protected'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
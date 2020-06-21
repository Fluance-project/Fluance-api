from routes import app
from flask import Flask, jsonify, request, session, render_template, make_response
from functools import wraps

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


@app.route('/api/v1/auth')
@check_for_token
def authorised():
    """
    This page has been created to test the token only
    :return:
    """
    return 'page protected'
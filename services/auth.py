import jwt
from bson.objectid import ObjectId
from flask import Flask, jsonify, request, session, render_template, make_response
from services import db
from functools import wraps
from config import SECRET

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        print(request.headers)
        try:
            token = request.headers['Authorization'].replace('Bearer ', '')
        except KeyError:
            return jsonify({'message': 'Missing token'}), 403

        try:
            data = jwt.decode(token, SECRET)
        except:
            return jsonify({'message' : 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped

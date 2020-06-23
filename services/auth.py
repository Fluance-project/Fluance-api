import jwt
from bson.objectid import ObjectId
from flask import Flask, jsonify, request, session, render_template, make_response
from services import db
from functools import wraps
from config import SECRET

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers['Authorization'].replace('Bearer ', '')
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            print(SECRET)
            data = jwt.decode(token, SECRET)
        except:
            return jsonify({'message' : 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped
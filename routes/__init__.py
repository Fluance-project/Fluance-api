"""This is init module."""
from flask import Flask
from flask_cors import CORS

# Place where app is defined
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['SECRET_KEY'] = 'Fluance'

from routes import root
from routes import account
from routes import machine
from routes import task
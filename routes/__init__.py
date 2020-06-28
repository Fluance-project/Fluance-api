"""This is init module."""
from flask import Flask
from flask_cors import CORS

# Place where app is defined
app = Flask(__name__)
cors = CORS(app)

from routes import root
from routes import account
from routes import machine
from routes import task
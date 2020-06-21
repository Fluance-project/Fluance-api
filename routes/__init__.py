"""This is init module."""
from flask import Flask

# Place where app is defined
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fluance'

from routes import root
from routes import account
from routes import machine
from routes import task
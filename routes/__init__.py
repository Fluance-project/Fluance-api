"""This is init module."""
from flask import Flask
from flask_cors import CORS

# Place where app is defined
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:root@54.92.140.66:27017/fluance?authSource=admin"
cors = CORS(app)

from routes import root
from routes import account
from routes import machine
from routes import task
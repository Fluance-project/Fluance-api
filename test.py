from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:root@54.92.140.66:27017/fluance"
mongo = PyMongo(app)
online_users = mongo.db.accounts.insert_one()
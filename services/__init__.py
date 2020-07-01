from flask_pymongo import PyMongo
from config import DATABASE_URI
from routes import app

mongo = PyMongo(app)
db = mongo.db
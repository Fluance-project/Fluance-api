from pymongo import MongoClient
from config import DATABASE_URI

client = MongoClient(f'{DATABASE_URI}')
db = client.fluance
import os

from pymongo.mongo_client import MongoClient

uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/search-engine')

# Create a new client and connect to the server
client = MongoClient(uri)

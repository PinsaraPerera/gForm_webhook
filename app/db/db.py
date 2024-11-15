from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.core.config import MONGO_USER, MONGO_PASSWORD, MONGO_CLUSTER

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}.ec2ws41.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.foss_db
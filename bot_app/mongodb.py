from pymongo import MongoClient
from os import urandom
from hashlib import sha256

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/", 
                    username='root',
                    password='root')
# Create database named "appdb"
db = client.appdb
# Create a collection named "users"
users_collection = db["users"]

def hashing_attribute(attribute):
    """
    Function that potentialy can hash 
    any attribute before adding to the DB
    """
    # Generate a random salt
    salt = urandom(16)

    # Hash the token using SHA-256 algorithm and salt
    hashed_attribute = sha256(salt + attribute.encode('utf-8')).hexdigest()

    return hashed_attribute

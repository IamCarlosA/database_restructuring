from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv('MONGODB_URL')
DB_NAME = os.getenv('DB_NAME')

if MONGODB_URL is None or DB_NAME is None:
    raise Exception("Environment variables are not set correctly")


def get_connection():
    client = MongoClient(MONGODB_URL)
    db = client[DB_NAME]
    print("Connection done!")
    return client, db

from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import os

uri = os.getenv("MONGOURI")


class VERIFY_USER:
    _connection = None

    def __init__(self):
        if VERIFY_USER._connection is None:
            VERIFY_USER._connection = MongoClient(uri)

        self.client = VERIFY_USER._connection
        self.db = self.client["CelestialGlimpse"]
        self.collection = self.db["Users_Email_Verify"]
        self.collection.create_index("email", unique=True)
        try:
            self.collection.drop_index('expireAt_1')
        except:
            pass
        self.collection.create_index("expireAt", expireAfterSeconds=0)

    def create_user(self, email):
        expire_date = datetime.utcnow() + timedelta(minutes=10)
        user = {
            "email": email,
            "expireAt": expire_date
        }
        try:
            result = self.collection.insert_one(user)
        except Exception as e:
            print(f"Error: {e}")
            return None
        return result.inserted_id

    def delete_user(self, ID):
        result = self.collection.delete_one({'_id': ID})
        if result.deleted_count == 0:
            return None
        return result.deleted_count

    def get_user(self, Id):
        users = self.collection.find_one({"_id": ObjectId(Id)})
        if users is None:
            return None
        return users


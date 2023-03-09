from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import os

# MongoDb Connection string
uri = os.getenv("MONGOURI")

# This class handles all user based functions for the users that are going through the verification process
class VERIFY_USER:
    _connection = None

    def __init__(self):
        # Connecting to MongoDb
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

    # Creating users in the verification colection
    def create_user(self, email):
        # Creating user with a expiration time of 10 minutes
        expire_date = datetime.utcnow() + timedelta(minutes=10)
        user = {
            "email": email,
            "expireAt": expire_date
        }
        # Trying to insert
        try:
            result = self.collection.insert_one(user)
        except Exception as e:
            # In case user is present
            print(f"Error: {e}")
            return None
        return result.inserted_id

    # Deleting user (if the verification process is complete
    def delete_user(self, ID):
        result = self.collection.delete_one({'_id': ID})
        if result.deleted_count == 0:
            return None
        return result.deleted_count

    # Getting user's by ID
    def get_user(self, Id):
        users = self.collection.find_one({"_id": ObjectId(Id)})
        if users is None:
            return None
        return users


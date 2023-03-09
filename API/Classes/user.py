from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os

# MongoDB Atlas Connection string
uri = os.getenv("MONGOURI")

'''There maybe a lot of unused code in this class, Which will be removed in future updates. Any contribution would be helpful'''

# This class handles all user events (in the main collection)
class USER:
    _connection = None

    def __init__(self):
        # Connecting to MongoDB
        if USER._connection is None:
            USER._connection = MongoClient(uri)

        self.client = USER._connection
        self.db = self.client["CelestialGlimpse"]
        self.collection = self.db["Users"]
        self.collection.create_index("email", unique=True)

    # Creating User (after verification process is done)
    def create_user(self, email):
        # Adding a placeholder datetime field
        dt = datetime.datetime(2008, 4, 6, 0, 0, 0)
        dt_oid = ObjectId.from_datetime(dt)
        user = {
            "email": email,
            "received": dt_oid
        }
        # Trying to insert the user in the database
        try:
            result = self.collection.insert_one(user)
        except Exception as e:
            # Handle the case where the email address is already in use
            print(f"Error: {e}")
            return None
        return result.inserted_id

    # Deleting users (after the verification process is done)
    def delete_user(self, ids=None):
        # Trying to delete
        result = self.collection.delete_one({'_id': ObjectId(ids)})
        if result.deleted_count == 0:
            # In case the user is not present
            return None
        return result.deleted_count

    # Updating the user's datetime object
    def update_user(self, email=None, received=None):
        update_query = {}
        dt_oid = ObjectId.from_datetime(received)
        update_query['received'] = dt_oid

        user = self.collection.find_one({'email': email})
        if user is None:
            raise ValueError(f"No user with email {email} found")

        result = self.collection.update_one({'email': user['email']}, {'$set': update_query})
        if result.modified_count == 0:
            raise ValueError(f"No user with ID {email} found")
        return result.modified_count

    # Striping time
    def striptime(self, email):
        user = self.collection.find_one({"email": email})
        if user:
            received_time = user["received"].generation_time.replace(tzinfo=None)
            return received_time
        return None

    # Getting users that do not match the current APOD's date
    def get_users(self, date=None, email=None):
        if date is None:
            users = self.collection.find_one({"email": email})
            if users is None:
                return None
            return users
        users = self.collection.find({"received": {"$ne": ObjectId.from_datetime(date)}})
        return users

    # Getting users with their id
    def get_users_with_id(self, IDS):
        users = self.collection.find_one({"_id": ObjectId(IDS)})
        if users is None:
            return None
        return users

from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os

uri = os.getenv("MONGOURI")


class USER:
    _connection = None

    def __init__(self):
        if USER._connection is None:
            USER._connection = MongoClient(uri)

        self.client = USER._connection
        self.db = self.client["CelestialGlimpse"]
        self.collection = self.db["Users"]
        self.collection.create_index("email", unique=True)

    def create_user(self, email):
        dt = datetime.datetime(2008, 4, 6, 0, 0, 0)
        dt_oid = ObjectId.from_datetime(dt)
        user = {
            "email": email,
            "received": dt_oid
        }
        try:
            result = self.collection.insert_one(user)
        except Exception as e:
            # Handle the case where the email address is already in use
            print(f"Error: {e}")
            return None
        return result.inserted_id

    def delete_user(self, email=None, ids=None):
        if ids is not None:
            result = self.collection.delete_one({'_id': ObjectId(ids)})
            if result.deleted_count == 0:
                return None
            return result.deleted_count

        result = self.collection.delete_one({'email': email})
        if result.deleted_count == 0:
            raise ValueError(f"No user with email {email} was found")
        return result.deleted_count

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

    def striptime(self, email):
        user = self.collection.find_one({"email": email})
        if user:
            received_time = user["received"].generation_time.replace(tzinfo=None)
            return received_time
        return None

    def get_users(self, date=None, email=None):
        if date is None:
            users = self.collection.find_one({"email": email})
            if users is None:
                return None
            return users
        users = self.collection.find({"received": {"$ne": ObjectId.from_datetime(date)}})
        return users

    def get_users_with_id(self, IDS):
        users = self.collection.find_one({"_id": ObjectId(IDS)})
        if users is None:
            return None
        return users

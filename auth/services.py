from .utils import hash_password
from .schemas import User, USER_COLLECTION
from database.connection import MongoClient

def create_user(user_obj):
    try:
        user_obj["password"] = hash_password(user_obj.pop("password"))
        user_id = MongoClient().insert_one(USER_COLLECTION, user_obj)
    except Exception:
        user_id = ""

    try:
        user_obj.pop("password")
    except Exception:
        pass
    
    return str(user_id)
    

def get_user(data):
    try:
        user_obj = MongoClient().find_one(USER_COLLECTION, data)
        if user_obj:
            user_obj["_id"] = str(user_obj["_id"])
    except Exception:
        user_obj = None

    return user_obj


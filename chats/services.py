from .schemas import Chat, CHAT_COLLECTION
from database.connection import MongoClient


def create_chat(chat_obj):
    try:
        chat_id = MongoClient().insert_one(CHAT_COLLECTION, chat_obj)
        return str(chat_id)
    except Exception:
        return None


def get_chat(data):
    try:
        chat_obj = MongoClient().find_one(CHAT_COLLECTION, data)
        if chat_obj:
            chat_obj["_id"] = str(chat_obj["_id"])
    except Exception:
        chat_obj = None
    return chat_obj


def get_chats_list(user_id, search={}, skip=0, limit=None, sort={"created_at": -1}):
    try:
        chat_objs = list(
            MongoClient().find(
                CHAT_COLLECTION,
                {"user_id": user_id, **search},
                skip=skip,
                limit=limit,
                sort=sort,
            )
        )
        for obj in chat_objs:
            obj["_id"] = str(obj.get("_id"))
    except Exception:
        chat_objs = []
    return chat_objs

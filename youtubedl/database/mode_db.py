import pymongo
from config.config import DB_URI

mongo_client = pymongo.MongoClient(DB_URI)
db = mongo_client["playlistmode"]
user_mode = db["user_settings"]

def get_normal_download_status(user_id):
    user_data = user_mode.find_one({"_id": user_id})
    status = user_data.get("normal_download") if user_data else None
    return status

def set_normal_download_status(user_id, status):
    user_mode.update_one(
        {"_id": user_id},
        {"$set": {"normal_download": status}},
        upsert=True
    )

def get_playlist_download_status(user_id):
    user_data = user_mode.find_one({"_id": user_id})
    status = user_data.get("playlist_download") if user_data else None
    return status

def set_playlist_download_status(user_id, status):
    user_mode.update_one(
        {"_id": user_id},
        {"$set": {"playlist_download": status}},
        upsert=True
    )

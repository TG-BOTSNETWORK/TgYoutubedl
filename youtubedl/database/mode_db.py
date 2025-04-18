from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://VEEZWORKS:SANTHU7981@veezworks.stpqs.mongodb.net/?retryWrites=true&w=majority&appName=veezworks")
db = client['pytgcalls_db']

def Connect(collection_name, operation, data=None, query=None, update=None, fetch=False):
    collection = db[collection_name]

    if operation == "insert":
        result = collection.insert_one(data)
        return result.inserted_id
    elif operation == "find":
        return list(collection.find(query)) if fetch else None
    elif operation == "update":
        result = collection.update_one(query, update, upsert=True)
        return collection.find_one(query) if fetch else None

def save_on_off(user_id, normal_status=None, playlist_status=None):
    normal_status = normal_status if normal_status is not None else False
    playlist_status = playlist_status if playlist_status is not None else False
    query = {"user_id": user_id}
    update = {
        "$set": {
            "normal_download_status": normal_status,
            "playlist_download_status": playlist_status
        }
    }
    result = Connect("download_status", "update", query=query, update=update, fetch=True)
    return {
        "normal_download_status": result["normal_download_status"],
        "playlist_download_status": result["playlist_download_status"]
    } if result else None

def get_is_on_off(user_id, mode=None):
    query = {"user_id": user_id}
    projection = {}
    if mode == "nrml":
        projection["normal_download_status"] = 1
    elif mode == "playlist":
        projection["playlist_download_status"] = 1
    else:
        projection["normal_download_status"] = 1
        projection["playlist_download_status"] = 1
    projection["_id"] = 0
    result = Connect("download_status", "find", query=query, fetch=True)
    if result:
        result = result[0]
        if len(projection) == 2:  # Only one field + _id
            return result.get("normal_download_status") or result.get("playlist_download_status")
        return {
            "normal_download_status": result["normal_download_status"],
            "playlist_download_status": result["playlist_download_status"]
        }
    return None

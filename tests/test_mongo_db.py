import os
from urllib.parse import quote_plus
from pymongo import MongoClient, ASCENDING
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

# --- Connection ---
def get_mongo_client():
    # For MongoDB Atlas use: "mongodb+srv://user:pass@cluster.mongodb.net/"
    user = quote_plus(os.environ["MONGO_USER"])
    password = quote_plus(os.environ["MONGO_PASSWORD"])
    host = os.environ["MONGO_HOST"]
    port = os.getenv("MONGO_PORT", "27017")
    uri = f"mongodb://{user}:{password}@{host}:{port}"
    client = MongoClient(uri)
    return client

# --- Query documents ---
def mongo_find():
    client = get_mongo_client()
    db_name = os.getenv("MONGO_DATABASE", "mydb")
    db = client[db_name]
    collection_name = os.getenv("MONGO_COLLECTION", "users")
    collection = db[collection_name]

    # # Find with filter
    # for doc in collection.find({"age": {"_id": "AH-TRX-3252-367408732300544"}}).limit(10):
    #     print(doc)

    # # Find one
    # user = collection.find_one({"email": "alice@example.com"})
    # print(user)

    # Find by ObjectId
    user = collection.find_one({"_id": "AH-TRX-3252-367408732300544"})
    print(user)

    client.close()

# # --- Insert ---
# def mongo_insert(name, email, age):
#     client = get_mongo_client()
#     db = client["mydb"]
#     collection = db["users"]

#     # Insert one
#     result = collection.insert_one({"name": name, "email": email, "age": age})
#     print(f"Inserted id: {result.inserted_id}")

#     # Insert many
#     result = collection.insert_many([
#         {"name": "Bob", "email": "bob@example.com", "age": 25},
#         {"name": "Carol", "email": "carol@example.com", "age": 30},
#     ])
#     print(f"Inserted ids: {result.inserted_ids}")

#     client.close()

# # --- Update ---
# def mongo_update(email, new_age):
#     client = get_mongo_client()
#     db = client["mydb"]
#     collection = db["users"]

#     result = collection.update_one(
#         {"email": email},
#         {"$set": {"age": new_age}}
#     )
#     print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

#     client.close()

# # --- Delete ---
# def mongo_delete(email):
#     client = get_mongo_client()
#     db = client["mydb"]
#     collection = db["users"]

#     result = collection.delete_one({"email": email})
#     print(f"Deleted count: {result.deleted_count}")

#     client.close()

# # --- Aggregation ---
# def mongo_aggregate():
#     client = get_mongo_client()
#     db = client["mydb"]
#     collection = db["users"]

#     pipeline = [
#         {"$match": {"age": {"$gte": 18}}},
#         {"$group": {"_id": "$age", "count": {"$sum": 1}}},
#         {"$sort": {"_id": ASCENDING}}
#     ]
#     for doc in collection.aggregate(pipeline):
#         print(doc)

#     client.close()

if __name__ == "__main__":
    mongo_find()
    # mongo_insert("Alice", "alice@example.com", 28)
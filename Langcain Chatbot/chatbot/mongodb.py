from pymongo import MongoClient

def get_mongo_client():
    return MongoClient("mongodb://localhost:27017")

def save_vector_store(data, collection_name):
    client = get_mongo_client()
    db = client['chatbot_db']
    collection_name = db['chatbot_data']
    collection_name.insert_many(data)

def get_messages(collection_name):
    client = get_mongo_client()
    db = client['chatbot_db']
    collection_name = db["chatbot_data"]
    messages = collection_name.find()
    return list(messages)

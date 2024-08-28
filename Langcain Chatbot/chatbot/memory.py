from langchain_mongodb import MongoDBChatMessageHistory
import pymongo

from chatbot.mongodb import get_mongo_client

def get_chat_memory(session_id: str):
    connection_string = "mongodb://localhost:27017"  # Replace with your MongoDB connection string
    chat_memory = MongoDBChatMessageHistory(
        connection_string=connection_string,
        database_name="chatbot_db",
        collection_name="chat_memory",
        session_id=session_id
    )
    messages = chat_memory.load_messages()
    return messages




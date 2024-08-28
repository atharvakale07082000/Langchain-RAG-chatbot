from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import List
from chatbot.chatbot import Chatbot

app = FastAPI()

# A dictionary to store Chatbot instances by session_id
chatbot_instances = {}

class QueryRequest(BaseModel):
    query: str
    session_id: str

@app.post("/upload")
async def upload(session_id: str = Form(...), files: List[UploadFile] = File(...)):
    # Ensure the Chatbot instance exists for the session_id
    if session_id not in chatbot_instances:
        chatbot_instances[session_id] = Chatbot(session_id)

    bot = chatbot_instances[session_id]
    
    try:
        for file in files:
            # Read file content asynchronously
            content = await file.read()

            # Pass the filename and content to load_documents
            bot.load_documents(file.filename, content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing error: {str(e)}")

    return {"message": "Files processed successfully"}

@app.post("/query")
async def query_bot(request: QueryRequest):
    # Ensure the Chatbot instance exists for the session_id
    if request.session_id not in chatbot_instances:
        raise HTTPException(status_code=404, detail="Session not found")
    
    bot = chatbot_instances[request.session_id]
    
    try:
        # Get response from the bot based on the query
        response = bot.answer_query(request.query)
    except Exception as e:
        # Return an HTTP 500 error with the exception details
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    
    return {"response": response}

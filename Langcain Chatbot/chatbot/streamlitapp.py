import streamlit as st
import requests
import time

# Set up the FastAPI backend URL
API_URL = "http://localhost:8000"

# Page Configuration
st.set_page_config(page_title="LangChain Chatbot", layout="wide")

# Title of the app
st.title("LangChain Chatbot with FastAPI Backend")

# --- Session Management ---
st.sidebar.header("Session Management")
session_list = ["default_session", "session_1", "session_2", "Create New Session"]
selected_session = st.sidebar.selectbox("Select or Create a Session", session_list)

if selected_session == "Create New Session":
    new_session_name = st.sidebar.text_input("New Session Name")
    if st.sidebar.button("Create Session") and new_session_name:
        selected_session = new_session_name
        st.sidebar.success(f"Session '{new_session_name}' created!")

# --- Sidebar for File Uploads ---
st.sidebar.header("Upload Documents")
uploaded_files = st.sidebar.file_uploader("Upload your documents", type=['pdf', 'docx', 'txt'], accept_multiple_files=True)

if st.sidebar.button("Process Documents"):
    if uploaded_files and selected_session:
        file_data = []
        for file in uploaded_files:
            file_data.append(('files', (file.name, file, file.type)))
        
        progress_bar = st.sidebar.progress(0)  # Initialize the progress bar
        progress_step = 100 // len(uploaded_files)  # Progress increment step
        
        # Call the FastAPI endpoint to upload and process files
        for idx, file in enumerate(uploaded_files):
            time.sleep(1)  # Simulate some processing time
            progress_bar.progress((idx + 1) * progress_step)  # Update progress

        response = requests.post(f"{API_URL}/upload/", data={'session_id': selected_session}, files=file_data)
        
        if response.status_code == 200:
            st.sidebar.success("Documents processed successfully!")
        else:
            st.sidebar.error("Error processing documents")
        
        progress_bar.empty()  # Clear the progress bar
    else:
        st.sidebar.warning("Please upload files and provide a session ID")

# --- Main Area for Chat with the Bot ---
st.header("Chat with the Bot")
user_input = st.text_input("Ask your question")

# Chat History Display
st.subheader(f"Chat History for session '{selected_session}'")

if st.button("Send"):
    if user_input and selected_session:
        # Call the FastAPI endpoint to query the chatbot
        response = requests.post(f"{API_URL}/query/", json={'session_id': selected_session, 'query': user_input})
        
        if response.status_code == 200:
            answer = response.json().get("response", "")
            st.success(f"Bot: {answer}")
            # Update chat history display
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            st.session_state.chat_history.append({"user": user_input, "bot": answer})
        else:
            st.error("Error getting response from the bot")
    else:
        st.warning("Please enter a question and provide a session ID")

# Display the chat history for the current session
if "chat_history" in st.session_state and st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.markdown(f"**User:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.markdown("---")

# Footer
st.markdown("---")
st.markdown("Built with LangChain, FastAPI, and Streamlit")

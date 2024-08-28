import streamlit as st
import requests

# Set up the FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

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
uploaded_files = st.sidebar.file_uploader("Upload your documents", type=['pdf', 'docx'], accept_multiple_files=True)

if st.sidebar.button("Process Documents"):
    if uploaded_files and selected_session:
        file_data = [('files', (file.name, file, file.type)) for file in uploaded_files]

        # Include the session ID as form data
        data = {'session_id': selected_session}

        # Call the FastAPI endpoint to upload and process files
        try:
            response = requests.post(f"{API_URL}/upload", data=data, files=file_data)
            
            if response.status_code == 200:
                st.sidebar.success("Documents processed successfully!")
            else:
                st.sidebar.error(f"Error processing documents: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.sidebar.error(f"An error occurred: {str(e)}")
    else:
        st.sidebar.warning("Please upload files and provide a session ID")

# --- Main Area for Chat with the Bot ---
st.header("Chat with the Bot")
user_input = st.text_input("Ask your question")

# Chat History Display
st.subheader(f"Chat History for session '{selected_session}'")

# Initialize chat history in session state if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Send"):
    if user_input and selected_session:
        # Call the FastAPI endpoint to query the chatbot
        try:
            response = requests.post(f"{API_URL}/query", json={'session_id': selected_session, 'query': user_input})
            
            if response.status_code == 200:
                answer = response.json().get("response", "")
                st.session_state.chat_history.append({"user": user_input, "bot": answer})
                st.success(f"Bot: {answer}")
            else:
                st.error(f"Error getting response from the bot: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a question and provide a session ID")

# Display the chat history for the current session
if st.session_state.chat_history:
    for chat in st.session_state.chat_history:
        st.markdown(f"**User:** {chat['user']}")
        st.markdown(f"**Bot:** {chat['bot']}")
        st.markdown("---")

# Footer
st.markdown("---")
st.markdown("Built with LangChain, FastAPI, and Streamlit")

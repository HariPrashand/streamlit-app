import streamlit as st
import os
from gradio_client import Client


def get_gradio_client():
    hf_token = st.secrets.get("huggingface", {}).get("api_key") or os.getenv("HF_API_KEY")
    client_kwargs = {"hf_token": hf_token} if hf_token else {}
    return Client("Sanaullah1122/health", **client_kwargs)

# Function to get chat response
def get_chat_response(user_input):
    try:
        client = get_gradio_client()
        response = client.predict(
            symptoms=user_input,
            language_choice="English 🇬🇧",
            api_name="/predict"
        )
        return str(response)
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
st.title("🤖 AI Chatbot")
st.write("Chat with an AI-powered assistant!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("Enter your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get and display AI response
    with st.chat_message("assistant"):
        response = get_chat_response(user_input)
        st.markdown(response)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

import streamlit as st
from huggingface_hub import InferenceClient

# Load API Key from Streamlit Secrets
HF_API_KEY = "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"
# Initialize Hugging Face API client
client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HF_API_KEY)

# Function to get chat response
def get_chat_response(user_input):
    try:
        response = client.text_generation(user_input, max_new_tokens=1024, temperature=0.7, top_p=0.7)
        return response
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
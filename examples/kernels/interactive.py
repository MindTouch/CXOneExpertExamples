# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
# streamlit run .\examples\kernels\interactive.py
import streamlit as st
from main import completions_kernels, get_deki_token
from dotenv import dotenv_values

# Retrieve credentials from environment variables
env_vars = dotenv_values("examples/kernels/.env")
domain = env_vars.get('DOMAIN')
api_key = env_vars.get('API_KEY')
secret_key = env_vars.get('SECRET_KEY')
username = env_vars.get('USERNAME')

st.title("KB chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(completions_kernels(
            prompt, domain, get_deki_token(api_key, secret_key, username)))

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

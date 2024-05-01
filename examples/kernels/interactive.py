# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
# streamlit run .\examples\kernels\interactive.py
import streamlit as st
from common import completions_kernels, get_deki_token
from dotenv import dotenv_values

# Retrieve credentials from environment variables
env_vars = dotenv_values("examples/kernels/.env")
domain = env_vars.get('DOMAIN')
api_key = env_vars.get('API_KEY')
secret_key = env_vars.get('SECRET_KEY')
username = env_vars.get('USERNAME')

st.title("Knowledge (single shot) chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask us anything about our knowledge"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner('loading...'):
            completion = completions_kernels(
                prompt, domain, token=get_deki_token(api_key, secret_key, username))
            response = st.write(completion['response']['completion'])

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

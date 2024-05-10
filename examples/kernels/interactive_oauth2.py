# https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps
# streamlit run .\examples\kernels\interactive_oauth2.py
import streamlit as st
from common import completions_kernels
from dotenv import dotenv_values
import requests
import os
from pprint import pprint

# Retrieve credentials from environment variables
env_vars = dotenv_values("examples/kernels/.env")
DOMAIN = env_vars.get('DOMAIN')
SSO_AUTH_ID = env_vars.get('SSO_AUTH_ID')
AUTHORIZATION_URL = f'{DOMAIN}@app/auth/{SSO_AUTH_ID}/token/authorize'
TOKEN_URL = f'{DOMAIN}@app/auth/{SSO_AUTH_ID}/token/access.json'
CLIENT_ID = env_vars.get('OAUTH2_KEY')
CLIENT_SECRET = env_vars.get('OAUTH2_SECRET')
REDIRECT_URI = env_vars.get('REDIRECT_URI')
SCOPE = "profile"

st.title("Knowledge (single shot) chat")

def chat_ux():

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
        response = None
        with st.chat_message("assistant"):
            completion = None
            with st.spinner('loading...'):
                completion = completions_kernels(
                    prompt, DOMAIN, authorization=st.session_state['authorization'])
                response = completion['response']['completion']
                if response is not None:
                    for page in completion['response']['pages']['page']:
                        nl = '  \n'
                        response = f"{response}{nl}Page {page['uri.ui']}"
                else:
                    response = 'No knowledge found.'
                st.write(response)


        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})


# Perform OpenID Connect OAuth2 flow for user access. https://success.mindtouch.com/Integrations/API/Authorization_Tokens/Use_an_OAuth_API_Token_With_an_Integration
if 'authorization' in st.session_state:
    chat_ux()
else:
    import base64
    if st.query_params.get('code') is not None:
        data = {
            'code': st.query_params["code"],
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
        }
        authorization_header = f"Basic {base64.b64encode((CLIENT_ID+ ':' + CLIENT_SECRET).encode()).decode()}"
        response = requests.post(f'{TOKEN_URL}', data=data, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': authorization_header,
        })
        if response.status_code == 200:
            st.session_state['authorization'] = f"{response.json()['token_type']} {response.json()['access_token']}"
            st.query_params.clear()
            chat_ux()
        elif response.status_code == 401:
            del st.session_state['authorization']
            st.rerun()
        else:
            response.raise_for_status()
    else:
        sso_url = f'{AUTHORIZATION_URL}?client_id={CLIENT_ID}&scope={SCOPE}&response_type=code&redirect_uri={REDIRECT_URI}'
        st.markdown(
            f'<a href="{sso_url}" target="_self">Login via SSO</a>', unsafe_allow_html=True)

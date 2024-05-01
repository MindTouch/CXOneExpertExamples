import requests
import xmltodict
import urllib.parse
from dotenv import dotenv_values
from common import get_deki_token


def search_kernels(query, domain, token):
    encoded_query = urllib.parse.quote(query)
    url = f"{domain}@api/deki/llm/kernels?q={encoded_query}&limit=50"
    headers = {
        'X-Deki-Token': token
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 responses
        result = xmltodict.parse(response.text)
        return result
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


if __name__ == '__main__':

    # Get input query from user
    query = input('Query: ')

    # Retrieve credentials from environment variables
    env_vars = dotenv_values("examples/kernels/.env")
    domain = env_vars.get('DOMAIN')
    api_key = env_vars.get('API_KEY')
    secret_key = env_vars.get('SECRET_KEY')
    username = env_vars.get('USERNAME')

    # Get Deki token
    token = get_deki_token(api_key, secret_key, username)

    # Perform search and handle response
    if token:
        result = search_kernels(query, domain, token)
        if result:
            print(result)
    else:
        print("Failed to retrieve Deki token.")

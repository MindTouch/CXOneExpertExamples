import requests
import urllib.parse
from dotenv import dotenv_values
import requests


def exchange_identity_token(identity_token_jwt, domain):
    """
    Exchange an identity token for a user session on a specified domain.

    Parameters:
    - identity_token_jwt (str): The JWT token provided by the identity provider.
    - domain (str): The domain where the token exchange should occur.

    Returns:
    - tuple: A tuple containing user information (dict) and the session (requests.Session) if successful,
             or (None, None) if the exchange failed.

    Raises:
    - requests.HTTPError: If the HTTP request returns a non-200 status code.
    - Exception: If the token exchange fails due to invalid credentials or other issues.

    Example:
    >>> identity_token_jwt = "..."  # Provide the actual identity token JWT
    >>> domain = "https://customer.mindtouch.com/"  # Provide the actual domain
    >>> user_info, session = exchange_identity_token(identity_token_jwt, domain)
    >>> if user_info:
    >>>     print(f"Welcome {user_info['fullname']}")
    >>>     # Use 'session' for additional requests as this user
    """

    # Endpoint for token exchange
    endpoint = f'{domain}@app/auth/token/exchange'

    # HTTP headers
    headers = {'Content-Type': 'application/json'}

    # Use requests.Session() for repeated requests
    with requests.Session() as session:
        try:
            # Exchange identity token for user session
            response = session.post(
                endpoint, data=identity_token_jwt, headers=headers)
            response.raise_for_status()  # Raise an error for non-200 status codes

            # Process user information if successful
            user = response.json()
            if not user.get('@anonymous', 'true').lower() == 'true':
                return user, session  # Return user information and session

            else:
                raise Exception('Token exchange failed: User is anonymous')

        except requests.RequestException as e:
            # Handle request exceptions
            raise requests.HTTPError(f"Token exchange request failed: {e}")

        except Exception as e:
            # Handle other exceptions
            raise Exception(f"Token exchange failed: {e}")


def search_kernels(query, domain, session):
    encoded_query = urllib.parse.quote(query)
    url = f"{domain}@api/deki/llm/kernels?q={encoded_query}&?dream.out.format=json"
    try:
        response = session.get(url)
        response.raise_for_status()  # Raise an exception for non-200 responses
        return response.json()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


if __name__ == '__main__':

    # Get input query from user
    query = input('Query: ')

    # Retrieve credentials from environment variables
    env_vars = dotenv_values("examples/kernels/.env")
    domain = env_vars.get('DOMAIN')
    identity_token_jwt = "REPLACEME"

    # Get Session
    user_info, session = exchange_identity_token(identity_token_jwt, domain)
    if user_info:
        print(f"Welcome {user_info['fullname']}")

        # Perform search and handle response
        result = search_kernels(query, domain)
        if result:
            print(result)

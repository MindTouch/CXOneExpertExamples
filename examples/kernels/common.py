import urllib.parse
import requests
import xmltodict


def get_deki_token(key: str, secret: str, user: str) -> str:
    """
    Get a token as user using server token key/secret
    """
    import hashlib
    import time
    import hmac

    epoch = str(int(time.time()))
    message_bytes = f'{key}_{epoch}_{user}'.encode('utf-8')
    secret_bytes = secret.encode('utf-8')
    hash = hmac.new(secret_bytes, message_bytes,
                    digestmod=hashlib.sha256).hexdigest().lower()
    return f'tkn_{key}_{epoch}_{user}_{hash}'


def completions_kernels(query, domain, token: str = None, authorization: str = None, limit: int = 100, threshold=0.5):
    encoded_query = urllib.parse.quote(query)
    url = f"{domain}@api/deki/llm/completion?q={encoded_query}&limit={limit}&threshold={threshold}"
    headers = {}
    if token is not None:
        headers['X-Deki-Token'] = token
    elif authorization is not None:
        headers['Authorization'] = authorization
    else:
        raise Exception('Missing token or authorization parameter')

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 responses
        return xmltodict.parse(response.text)
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

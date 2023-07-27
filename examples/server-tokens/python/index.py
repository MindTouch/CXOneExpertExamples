import hashlib
import time
import requests
import hmac

# Server API Token key and secret
key = 'REDACTED'
secret = 'REDACTED'

# include username prefixed with '=' or include userid
user = '=admin'
# user = '123'

# hash time, key, user with secret
epoch = str(int(time.time()))
message_bytes = f'{key}_{epoch}_{user}'.encode('utf-8')
secret_bytes = secret.encode('utf-8')
hash = hmac.new(secret_bytes, message_bytes, digestmod=hashlib.sha256).hexdigest().lower()
token = f'tkn_{key}_{epoch}_{user}_{hash}'

# send signature as X-Deki-Token HTTP header to MindTouch API (Python Requests is used in this example)
headers = {
   'X-Deki-Token': token,
}
response = requests.get('https://success.mindtouch.com/@api/deki/users/current', headers=headers, verify=False)

# Handling the response
if response.status_code == 200:
    # Success
    print(response.text)
else:
    # Error
    print(f"Error: {response.status_code} - {response.text}")

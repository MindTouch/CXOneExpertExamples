import hashlib
import time
import requests
import hmac
import urllib.parse
import xmltodict

key = 'REDACTED'
secret = 'REDACTED'
user = '=foo'
site = 'https://customer.mindtouch.com'

epoch = str(int(time.time()))
message_bytes = f'{key}_{epoch}_{user}'.encode('utf-8')
secret_bytes = secret.encode('utf-8')
hash = hmac.new(secret_bytes, message_bytes,
                digestmod=hashlib.sha256).hexdigest().lower()
token = f'tkn_{key}_{epoch}_{user}_{hash}'

# send signature as X-Deki-Token HTTP header to MindTouch API (Python Requests is used in this example)
headers = {
    'X-Deki-Token': token,
}

# Check if user exists
response = requests.get(
    f'{site}/@api/deki/users/current', headers=headers, verify=False)
response.raise_for_status()
xml = xmltodict.parse(response.text)

# this will create the user if it doesn't exist.
if xml['user']['username'] == 'Anonymous':
    response = requests.get(
        f'{site}/@api/deki/users/authenticate?x-deki-token={token}', headers=headers, verify=False)
    response.raise_for_status()

# Generate a link that a user can click that will authenticate and redirect to a file (only required once since the session has been created)
redirect_encoded = urllib.parse.quote(
    f"{site}/@api/deki/files/1/1ef17415582adac0a88cdf8171afc9c4.jpg", safe='')
print(
    f"User should click here now: {site}/@api/deki/users/authenticate?x-deki-token={token}&redirect={redirect_encoded}")

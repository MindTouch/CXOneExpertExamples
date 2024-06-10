import hashlib
import time
import requests
import hmac

# Server API Token key and secret
key = 'REDACTED'
secret = 'REDACTED'
domain = 'customer.mindtouch.us'

# include username prefixed with '=' or include userid
user = '=admin'

# hash time, key, user with secret
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
response = requests.get(
    f'https://{domain}/@api/deki/users/current?dream.out.format=json', headers=headers, verify=False)
response.raise_for_status()
if response.json()['@anonymous'] is not 'false':
    authenticate_exchange_response = requests.get(
        f'https://{domain}/@api/deki/users/authenticate?x-deki-token={token}', headers=headers, verify=False)
    authtoken = authenticate_exchange_response.cookies['authtoken']

    # token that can be passed to Expert as a cookie `authtoken`
    print(f'User authtoken session: {authtoken}')

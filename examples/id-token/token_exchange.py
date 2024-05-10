import requests

# an identity token jwt provided by the identity provider
identity_token_jwt = "REPLACEME"

# Expert site/domain
domain = 'customer.mindtouch.com'

# keep a session (for repeated requests as this user)
session = requests.Session()

# Exchange identity token for user session using a matching identity provider
response = session.post(
    f'https://{domain}/@app/auth/token/exchange',
    data=identity_token_jwt,
    headers={'Content-Type': 'application/json; charset=utf-8'}
)

if response.status_code == 200:

    # User has been provisioned based on the identity token.
    user = response.json()
    if user['@anonymous'] == 'false':
        print('Welcome ' + user['fullname'])

        # Additional requests as this user is now possible.
    else:
        raise Exception('Token exchanged failed')
else:
    response.raise_for_status()
    print(response.text)

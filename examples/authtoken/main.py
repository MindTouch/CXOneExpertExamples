# perform content changes at your own risk outside of the existing editor.
import requests

# Expert site/domain
domain = 'customer.mindtouch.com'

# keep a session (for repeated requests as this user)
session = requests.Session()

# set cookie from prior interaction (this can be retrieved using dekiscript's user.authtoken method.)
cookie_authtoken_name = 'authtoken'
cookie_authtoken_value = 'REDACTED'

# Add the cookie to the session
session.cookies.set(cookie_authtoken_name, cookie_authtoken_value)

# Get the current user session
current_user_url = f"https://{domain}/@api/deki/users/current?dream.out.format=json"
response = session.get(current_user_url)
response.raise_for_status()
user = response.json()
print(user)

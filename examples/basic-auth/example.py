import requests
import json
from pprint import pprint

fdqn = 'https://CUSTOMERDOMAIN.mindtouch.us/'
# Authenticate and save cookies to cookies.txt
auth_url = f"{fdqn}@api/deki/users/authenticate"
auth_credentials = ("REDACTED_USER", "REDACTED_PASSWORD")

# Make authentication request
auth_response = requests.get(auth_url, auth=auth_credentials)
auth_cookies = auth_response.cookies

# Save cookies to cookies.txt
with open('cookies.txt', 'w') as cookies_file:
    for cookie in auth_cookies:
        cookies_file.write(f"{cookie.name}={cookie.value}; ")

# Make a request to get current user information using the saved cookies
current_user_url = f"{fdqn}@api/deki/users/current?dream.out.format=json"
current_user_response = requests.get(current_user_url, cookies=auth_cookies)

# convert to json
current_user_json = json.loads(current_user_response.text)

# Print the response
pprint(current_user_json)

import requests

# Expert site/domain
domain = 'customer.mindtouch.com'

# keep a session (for repeated requests as this user)
session = requests.Session()

auth_url = f"https://{domain}@api/deki/users/authenticate"
auth_credentials = ("REDACTED_USER", "REDACTED_PASSWORD")

# Make auth request
auth_response = session.get(auth_url, auth=auth_credentials)
auth_response.raise_for_status()

current_user_response = requests.get(f"https://{domain}@api/deki/users/current")
current_user_response.raise_for_status()
print(current_user_response.text)


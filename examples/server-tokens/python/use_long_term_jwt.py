"""Use a long-term JWT (OAuth bearer token) for API authentication."""

import json
import requests
import time

JWT = "REPLACEME_WITH_YOUR_JWT"
DOMAIN = "https://example.mindtouch.es"


def decode_jwt_exp(jwt: str) -> int:
    """Extract expiration timestamp from JWT payload."""
    payload = jwt.split(".")[1]
    padding = 4 - len(payload) % 4
    if padding != 4:
        payload += "=" * padding
    import base64

    return int(json.loads(base64.urlsafe_b64decode(payload))["exp"])


response = requests.get(
    f"{DOMAIN}/@api/deki/users/current?dream.out.format=json",
    headers={"Authorization": f"Bearer {JWT}"},
    timeout=30,
)
user = response.json()

exp_timestamp = decode_jwt_exp(JWT)
expires_at = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(exp_timestamp))

print(f"User: {user.get('username')} (ID: {user.get('@id')})")
print(f"Email: {user.get('email')}")
print(f"Expires: {expires_at}")

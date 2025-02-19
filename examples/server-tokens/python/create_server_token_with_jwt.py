"""Create a server token with a restricted user id"""

import requests

PAYLOAD = """
<developer-token type='server'>
    <name>foo jwt</name>
    <restricted-by-user-id>1</restricted-by-user-id>
</developer-token>
"""
DOMAIN = "https://example.foo"
cookies = {
    "authtoken": "REPLACEME"
}
response = requests.post(
    f"{DOMAIN}/@api/deki/site/developer-tokens?dream.out.format=json",
    data=PAYLOAD,
    headers={"Content-Type": "application/xml"},
    verify=False,
    cookies=cookies,
    timeout=30,
)
print(response.text)

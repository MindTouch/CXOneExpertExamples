# Basic Authentication with Local Accounts

`curl https://success.mindtouch.com/@api/deki/users/authenticate -u "admin:REDACTED" --cookie-jar cookies.txt`

now use the cookie jar
`curl https://success.mindtouch.com/@api/deki/users/current?dream.out.format=json -b cookies.txt | jq`
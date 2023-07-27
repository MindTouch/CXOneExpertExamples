# OAuth2 using the Authorization Code Flow

Shows an OAuth2 authorization code flow with a nodejs backend. See [Use an OAuth API Token With an Integration](https://success.mindtouch.com/Integrations/API/Authorization_Tokens/Use_an_OAuth_API_Token_With_an_Integration) for technical docs.

## Quick Start 🚀

`npm install`

Make a copy of `configExample.json` to `config.json` then update with [prerequisites](https://success.mindtouch.com/Integrations/API/Authorization_Tokens/Use_an_OAuth_API_Token_With_an_Integration#Prerequisites).


```json
{
    "hostname": "// Hostname of site",
    "appHostname": "// hostname of this app (localhost does seem to be an issue with Chrome)",
    "authId": 1, // service provider id provided by support (1 is local support whereas any number after could be service provider id)
    "clientID": "// OAuth2 Client Id",
    "clientSecret": "// OAuth2 Client Secret",
    "scope": "profile seated",
    "port": 8098 // Host of this app
}
```

Example app config running locally using local authentication
```json
{
    "hostname": "success.mindtouch.us",
    "appHostname": "localhost",
    "authId": 1,
    "clientID": "9e1460b62e557fa35833bcf715fdb6a1980020c5ace6294ce1d0036250d0b9dc",
    "clientSecret": "46efb56f078c4c9303a036fa37bfc1459f96cade508675794ce9c8bef3af550f",
    "scope": "profile",
    "port": 8098
}

```

`node index.js`

Go to: [http://localhost:8080](http://localhost:8080)

## Resources

-   https://success.mindtouch.com/Integrations/API/Authorization_Tokens/Use_an_OAuth_API_Token_With_an_Integration
-   https://success.mindtouch.com/Integrations/API
-   https://success.mindtouch.com/Admin/Authentication/OpenID_Connect/OpenID_Connect_Relying_Party_Endpoints

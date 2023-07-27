const express = require('express');
const fetch = require('node-fetch');
const fs = require('fs');
const port = 8089;

// Local testing
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = 0;

let config = JSON.parse(fs.readFileSync(__dirname + '/config.json'));
config.accessTokenUrl = `https://${config.hostname}/@app/auth/${config.authId}/token/access.json`;
config.api = `https://${config.hostname}/@api/deki/`;
const redirectPath = '/oauth2/redirect';
config.redirectUri = `http://${config.appHostname}:${port}${redirectPath}`;
config.authorizeUrl = `https://${config.hostname}/@app/auth/${config.authId}/token/authorize?client_id=${config.clientID}&scope=${config.scope}&response_type=code&redirect_uri=${config.redirectUri}`;

// Web server instance
const app = express();
app.use(express.static(__dirname + '/public'));

// Endpoint with current configuration details
app.get('/config.json', (_req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.end(
        JSON.stringify({
            authorizeUrl: config.authorizeUrl,
            api: config.api,
        })
    );
});

let jwtByCode = {};

// After the user has been authorized, the callback with `redirectUri` is invoked with an authorization code.
app.get(redirectPath, async (req, res) => {
    // Retrieve the authorization JWT from identity provider
    const jwt = await requestAccessToken(req.query.code, config);

    // NOTE (2021-08-04, spencerk): for simplicity, store jwt in a key value object then remove it when retrieved. Using a cookie session would be better.
    jwtByCode[req.query.code] = jwt;

    // Redirect back to home with the code. Front end can now request it via token.json endpoint
    res.statusCode = 302;
    res.setHeader('Location', '/?code=' + req.query.code);
    res.end();
});

// Retrieve token with code ONCE.
app.get('/token.json', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    if (req.query.code && jwtByCode.hasOwnProperty(req.query.code)) {
        res.write(JSON.stringify(jwtByCode[req.query.code]));
        delete jwtByCode[req.query.code];
    } else {
        res.write(JSON.stringify({}));
    }
    res.end();
});

async function requestAccessToken(code, config) {
    const data = {
        code: code,
        grant_type: 'authorization_code', // eslint-disable-line camelcase
        client_id: config.clientID, // eslint-disable-line camelcase
        redirect_uri: config.redirectUri, // eslint-disable-line camelcase
    };
    try {
        const authorizationHeader = `Basic ${Buffer.from(config.clientID + ':' + config.clientSecret).toString(
            'base64'
        )}`;
        const response = await fetch(config.accessTokenUrl, {
            method: 'POST',
            body: new URLSearchParams(data),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                Authorization: authorizationHeader,
            },
        });
        if (!response.ok) {
            console.log(response);
            console.log(await response.text());
        }
        return await response.json();
    } catch (err) {
        console.warn('Unable to get an access token: ' + err); // eslint-disable-line no-console
        return JSON.stringify({});
    }
}

app.listen(port);

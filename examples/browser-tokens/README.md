
```javascript
async function request(url) {
  const key =
    "REDACTED";
  const response = await fetch(url, {
    headers: {
      "X-Deki-Token": key,
    },
  });
  const json = await response.json();
  console.log(json);
}

request(
  "https://success.mindtouch.com/@api/deki/pages/home/info?dream.out.format=json"
);
request(
  "https://success.mindtouch.com/@api/deki/users/current?dream.out.format=json"
);
```

Typical CORS message
`index.html:1 Access to fetch at 'https://example.com/@api/deki/pages/home/info?dream.out.format=json' from origin 'https://cdpn.io' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource. If an opaque response serves your needs, set the request's mode to 'no-cors' to fetch the resource with CORS disabled.`

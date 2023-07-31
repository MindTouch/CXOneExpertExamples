import os
import json
import base64
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), 'templates'))
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static')), name="static")
port = 8089

# Read the configuration from the 'config.json' file
with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
    config = json.load(config_file)

config['accessTokenUrl'] = f"https://{config['hostname']}/@app/auth/{config['authId']}/token/access.json"
config['api'] = f"https://{config['hostname']}/@api/deki/"
redirectPath = '/oauth2/redirect'
config['redirectUri'] = f"http://{config['appHostname']}:{port}{redirectPath}"
config['authorizeUrl'] = f"https://{config['hostname']}/@app/auth/{config['authId']}/token/authorize?client_id={config['clientID']}&scope={config['scope']}&response_type=code&redirect_uri={config['redirectUri']}"

jwtByCode = {}

async def request_access_token(code: str):
    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': config['clientID'],
        'redirect_uri': config['redirectUri'],
    }
    try:
        authorization_header = f"Basic {base64.b64encode((config['clientID'] + ':' + config['clientSecret']).encode()).decode()}"
        async with httpx.AsyncClient() as client:
            response = await client.post(config['accessTokenUrl'], data=data, headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': authorization_header,
            })
            if not response.is_success:
                print(response)
                print(response.text)
            return response.json()
    except Exception as err:
        print(f'Unable to get an access token: {err}')
        return {}

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/config.json")
async def get_config():
    return {
        'authorizeUrl': config['authorizeUrl'],
        'api': config['api']
    }

@app.get("/token.json")
async def get_token(code: str):
    if code in jwtByCode:
        jwt = jwtByCode[code]
        del jwtByCode[code]
        return jwt
    return {}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8089)

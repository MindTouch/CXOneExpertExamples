"""OAuth2 Authorization Code flow example for CXone Expert (MindTouch).

This FastAPI app demonstrates the OAuth2 Authorization Code flow against an
Expert site. The browser is redirected to the Expert authorization endpoint;
on success Expert redirects back to ``/oauth2/redirect`` with a ``code`` that
this app exchanges (server-side) for an access token.

See: https://success.mindtouch.com/Integrations/API/Authorization_Tokens/Use_an_OAuth_API_Token_With_an_Integration
"""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any

import httpx
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ---------------------------------------------------------------------------
# Constants and paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

REDIRECT_PATH = "/oauth2/redirect"
DEFAULT_PORT = 8089


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    """Load ``config.json`` and derive the OAuth2 endpoint URLs.

    The on-disk config contains only the site/app identity fields. This helper
    fills in the fully-qualified ``authorizeUrl``, ``accessTokenUrl``, ``api``,
    and ``redirectUri`` values used throughout the app.
    """
    with path.open(encoding="utf-8") as config_file:
        config: dict[str, Any] = json.load(config_file)

    port = config.get("port", DEFAULT_PORT)
    hostname = config["hostname"]
    auth_id = config["authId"]
    client_id = config["clientID"]
    scope = config["scope"]
    app_hostname = config["appHostname"]

    config["accessTokenUrl"] = (
        f"https://{hostname}/@app/auth/{auth_id}/token/access.json"
    )
    config["api"] = f"https://{hostname}/@api/deki/"
    config["redirectUri"] = f"http://{app_hostname}:{port}{REDIRECT_PATH}"
    config["authorizeUrl"] = (
        f"https://{hostname}/@app/auth/{auth_id}/token/authorize"
        f"?client_id={client_id}"
        f"&scope={scope}"
        f"&response_type=code"
        f"&redirect_uri={config['redirectUri']}"
    )
    return config


config = load_config()

# In-memory store mapping an authorization ``code`` to its exchanged JWT.
# The frontend reads the token via ``/token.json?code=...`` once, then it is
# discarded. This is fine for a demo but NOT suitable for production.
jwt_by_code: dict[str, dict[str, Any]] = {}


# ---------------------------------------------------------------------------
# FastAPI app setup
# ---------------------------------------------------------------------------

app = FastAPI(title="CXone Expert OAuth2 Example")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ---------------------------------------------------------------------------
# OAuth2 helpers
# ---------------------------------------------------------------------------


async def request_access_token(code: str) -> dict[str, Any]:
    """Exchange an authorization ``code`` for an access token (JWT).

    Sends an HTTP Basic-authenticated ``POST`` to the Expert access-token
    endpoint. Returns the decoded JSON response, or an empty dict on failure.
    """
    credentials = f"{config['clientID']}:{config['clientSecret']}".encode()
    authorization_header = f"Basic {base64.b64encode(credentials).decode()}"

    data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": config["clientID"],
        "redirect_uri": config["redirectUri"],
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": authorization_header,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config["accessTokenUrl"], data=data, headers=headers
            )
            if not response.is_success:
                print(f"Access token request failed: {response.status_code}")
                print(response.text)
            return response.json()
    except Exception as err:  # noqa: BLE001 - demo code, log and move on
        print(f"Unable to get an access token: {err}")
        return {}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request) -> HTMLResponse:
    """Render the single-page demo UI."""
    return templates.TemplateResponse(request, "index.html")


@app.get("/config.json")
async def get_config() -> dict[str, str]:
    """Expose only the public bits of the config to the browser."""
    return {
        "authorizeUrl": config["authorizeUrl"],
        "api": config["api"],
    }


@app.get(REDIRECT_PATH)
async def oauth2_redirect(code: str) -> RedirectResponse:
    """OAuth2 callback: exchange ``code`` for a JWT and bounce to the UI."""
    jwt_by_code[code] = await request_access_token(code)
    return RedirectResponse(url=f"/?code={code}")


@app.get("/token.json")
async def get_token(code: str) -> dict[str, Any]:
    """Return (and remove) the JWT associated with an authorization ``code``."""
    return jwt_by_code.pop(code, {})


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    port = int(os.environ.get("PORT") or config.get("port", DEFAULT_PORT))
    uvicorn.run(
        app,
        host="0.0.0.0",  # noqa: S104 - demo binds to all interfaces
        port=port,
    )

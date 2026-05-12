# OAuth2 using the Authorization Code Flow (Python)

Shows an OAuth2 authorization code flow with a Python/[FastAPI](https://fastapi.tiangolo.com/) backend. See [Use an OAuth API Token With an Integration](https://success.mindtouch.com/Integrations/API/Authorization_Tokens/Use_an_OAuth_API_Token_With_an_Integration) for the technical docs.

## Prerequisites

- Python 3.11+ (the included `.venv` was built with 3.13)
- [`uv`](https://docs.astral.sh/uv/) — fast Python package & project manager from Astral

Install `uv` (one-time):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# or via pipx / brew
pipx install uv
brew install uv
```

## Quick Start 🚀

From this directory (`examples/oauth2/python`):

```bash
# 1. Create the virtual environment and install dependencies from pyproject.toml
uv sync

# 2. Copy the example config and fill in your OAuth2 credentials
cp configExample.json config.json
$EDITOR config.json

# 3. Run the app
uv run python main.py
```

Then open [http://notlocalhost:8089](http://notlocalhost:8089).

> **Why not `localhost`?** Chrome (and some OAuth providers) treat `localhost` specially for cookies, redirect-URI matching, and third-party-context restrictions, which can break the redirect step. Map an alias such as `notlocalhost` to `127.0.0.1` and use that instead:
>
> ```bash
> # /etc/hosts  (or  C:\Windows\System32\drivers\etc\hosts)
> 127.0.0.1   notlocalhost
> ```
>
> Make sure `appHostname` in `config.json` matches the alias you use.

> `uv sync` reads `pyproject.toml`, creates `.venv/` if missing, resolves the dependency graph, and writes/updates `uv.lock` for reproducible installs. `uv run` executes a command inside that managed environment without needing to manually activate it.

### Common `uv` commands

| Task                                        | Command                                        |
| ------------------------------------------- | ---------------------------------------------- |
| Install / update deps from `pyproject.toml` | `uv sync`                                      |
| Add a new dependency                        | `uv add <package>`                             |
| Remove a dependency                         | `uv remove <package>`                          |
| Run a command in the project venv           | `uv run <cmd>`                                 |
| Run the app                                 | `uv run python main.py`                        |
| Run with hot reload (dev)                   | `uv run uvicorn main:app --reload --port 8089` |
| Upgrade locked versions                     | `uv lock --upgrade && uv sync`                 |
| Activate the venv manually (optional)       | `source .venv/bin/activate`                    |

## Configuration

Copy `configExample.json` to `config.json` and update using the values from the [prerequisites](https://success.mindtouch.com/Integrations/API/Authorization_Tokens/Use_an_OAuth_API_Token_With_an_Integration#Prerequisites):

```json
{
  "hostname": "// Hostname of the Expert site",
  "appHostname": "// hostname of this app (use an alias like 'notlocalhost' — Chrome treats 'localhost' specially)",
  "authId": 1,
  "clientID": "// OAuth2 Client Id",
  "clientSecret": "// OAuth2 Client Secret",
  "scope": "profile",
  "port": 8089
}
```

Example local config:

```json
{
  "hostname": "success.mindtouch.us",
  "appHostname": "notlocalhost",
  "authId": 1,
  "clientID": "9e1460b62e557fa35833bcf715fdb6a1980020c5ace6294ce1d0036250d0b9dc",
  "clientSecret": "46efb56f078c4c9303a036fa37bfc1459f96cade508675794ce9c8bef3af550f",
  "scope": "profile",
  "port": 8089
}
```

`config.json` is gitignored — it holds secrets and should never be committed.

## Project layout

```
.
├── main.py              # FastAPI app: auth redirect + token exchange
├── pyproject.toml       # Project + dependencies (managed by uv)
├── uv.lock              # Resolved dependency lockfile (created by `uv sync`)
├── config.json          # Your OAuth2 credentials (gitignored)
├── configExample.json   # Template config
├── templates/           # Jinja2 templates
└── static/              # Static assets
```

## Resources

- [Use an OAuth API Token With an Integration](https://success.mindtouch.com/Integrations/API/Authorization_Tokens/Use_an_OAuth_API_Token_With_an_Integration)
- [Integrations / API overview](https://success.mindtouch.com/Integrations/API)
- [OpenID Connect Relying Party Endpoints](https://success.mindtouch.com/Admin/Authentication/OpenID_Connect/OpenID_Connect_Relying_Party_Endpoints)
- [uv documentation](https://docs.astral.sh/uv/)

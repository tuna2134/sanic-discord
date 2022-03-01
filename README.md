# sanic-discord

## example

```python
from sanic import Sanic
from sanic.response import text
from sanic_discord import Client, Config

app = Sanic("app")
client = Client(
    Config(
        secret="secret",
        id="clientid",
        login_url="login url",
        callback_url="https://example.com/callback",
        redirect_url="/me"
    )
)

@app.route("/callback")
async def callback(request):
    return await client.callback(request)
    
@app.route("/me")
@client.oauth2_required()
async def me(request, user):
    return text(user["username"] + "hello")

app.run("0.0.0.0", 8000)
```

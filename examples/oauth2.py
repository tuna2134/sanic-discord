from sanic import Sanic, response
from sanic_discord import Oauth2

from os import getenv


app = Sanic("hello")
oauth2 = Oauth2(
    app, client_id=getenv("CLIENT_ID"), client_secret=getenv("CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8000/callback"
)


@app.get("/callback")
@oauth2.exchange_code()
async def redirect(_, access_token):
    r = response.json({"access_token": access_token.access_token})
    r.cookies["access_token"] = access_token.access_token
    r.cookies["access_token"]["expires"] = access_token.expires_in
    return r

@app.get("/login")
async def login(_):
    return response.redirect(oauth2.get_authorize_url(["identify", "email"]))

@app.get("/")
async def index(request):
    if "access_token" in request.cookies:
        return response.json(
            await oauth2.fetch_user(request.cookies["access_token"])
        )
    return response.redirect("/login")

@app.before_server_stop
async def close_client(app, loop):
    print("CLosing oauth client...")
    await oauth2.close()

app.run("0.0.0.0")
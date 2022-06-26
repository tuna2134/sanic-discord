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
async def redirect(request, access_token):
    r = response.json({"access_token": access_token.access_token})
    r.cookies["access_token"] = access_token.access_token
    r.cookies["access_token"]["expires"] = access_token.expires_in
    return r

app.run("0.0.0.0")
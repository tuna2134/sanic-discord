from sanic import Sanic, response

from sanic_discord import InteractionClient


app = Sanic(__name__)
client = InteractionClient(app, "token", "public_key")


@app.get("/")
async def basic(request):
    return response.text("foo")

@app.post("/interaction")
async def interaction(request):
    return await client.handle_interaction(request)

@client.on_interaction
async def on_interaction(data):
    pass

app.run(host="0.0.0.0")
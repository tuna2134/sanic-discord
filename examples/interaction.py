from sanic import Sanic, response

from sanic_discord import InteractionClient

from os import getenv


app = Sanic(__name__)
client = InteractionClient(
    app, getenv("CLIENT_TOKEN"), getenv("PUBLIC_KEY")
)


@app.get("/")
async def basic(request):
    return response.text("foo")

@app.post("/interaction")
async def interaction(request):
    return await client.handle_interaction(request)

@client.on_interaction
async def on_interaction(data):
    pass

app.run(host="0.0.0.0", port=8080)
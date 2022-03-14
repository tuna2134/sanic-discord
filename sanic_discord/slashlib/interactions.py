from sanic.response import json
from .types import User

class Interaction:
    def __init__(self, client, data):
        self.__data = data
        self.client = client

    @property
    def token(self):
        return self.__data["token"]

    @property
    def id(self):
        return self.__data["id"]

    @property
    def user(self):
        return User(self.__data["member"]["user"])

    @property
    def command(self):
        return InteractionCommand(self.__data["data"])

    @property
    def type(self):
        return self.__data["type"]

    def send(self, content=None, *,
             tts=None, embeds: list=None,
             ephemeral: bool=False):
        payload = {
            "type": 4,
            "data": {}
        }
        if content is not None:
            payload["data"]["content"] = content
        if tts is not None:
            payload["data"]["tts"] = True
        if embeds is not None:
            payload["data"]["embeds"] = [embed.payload for embed in embeds]
        if ephemeral is True:
            payload["flags"] = 1 << 6
        return json(payload)

    async def fetch_message(self):
        return InteractionMessage(self, await self.client.request("GET", f"/webhooks/829578365634740225/{self.token}/messages/@original"))

class InteractionMessage:
    def __init__(self, interaction, data):
        self._data = data
        self.interaction = interaction

    @property
    def id(self):
        return self._data["id"]

    @property
    def content(self):
        return self._data["content"]

    @property
    def channel_id(self):
        return self._data.get("channel_id")

    async def edit(self, content=None, *,
                   embeds: list=None):
        payload = {}
        if content is not None:
            payload["content"] = content
        if embeds is not None:
            payload["embeds"] = [embed.payload for embed in embeds]
        await self.interaction.client.request("PATCH", f"/webhooks/829578365634740225/{self.interaction.token}/messages/@original", json=payload)
    
class InteractionCommand:
    def __init__(self, data):
        self._data = data

    @property
    def options(self):
        if self._data.get("options"):
            return [InteractionCommandOption(d) for d in self._data["options"]]

    @property
    def name(self):
        return self._data["name"]

class InteractionCommandOption:
    def __init__(self, data):
        self._data = data

    @property
    def name(self):
        return self._data["name"]

    @property
    def value(self):
        return self._data["value"]

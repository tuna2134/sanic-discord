from .interactions import Interaction
from .types import User
from .types.commands import Command, CommandOption
from sanic.response import json, text
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from aiohttp import ClientSession
from importlib import import_module
from os import getenv
import asyncio

from typing import Optional

class ApiError(Exception):
    pass

class Bot:
    ApiUrl = "https://discord.com/api/v9"
    def __init__(self, app, token, publickey):
        self.web = app
        self.token = token
        self.publickey = publickey
        self.commands = []
        self.cogs = {}

    async def request(self, method: str,
                      path: str
                      , *args, **kwargs) -> Optional[dict]:
        headers = {
            "Authorization": "Bot {}".format(self.token)
        }
        kwargs["headers"] = headers
        for i in range(5):
            async with ClientSession(loop=self.loop) as session:
                async with session.request(method, self.ApiUrl + path, *args, **kwargs) as r:
                    if r.status == 404:
                        raise ApiError("404 error")
                    elif r.status == 200:
                        return await r.json()
                    elif r.status == 429:
                        if r.headers.get("Retry-After"):
                            await asyncio.sleep(int(r.headers["Retry-After"]))
                        else:
                            raise ApiError("rate limit!")
                    elif r.status == 500:
                        raise ApiError("500 error")

    async def if_finish(self, conn_info):
        if conn_info.ctx.path == "/interaction":
            conn_info.ctx._wait_response.set()

    async def fetch_user(self, id):
        return User(await self.request("GET", f"/users/{id}"))

    async def process_slash_command(self, name: str,
                                    interaction: Interaction):
        for command in self.commands:
            if command.name == name:
                interaction.request.conn_info.ctx._wait_response = asyncio.Event()
                asyncio.create_task(self._wait_response(interaction, command))
                kwargs = {}
                if interaction.command.options:
                    for option in interaction.command.options:
                        kwargs[option.name] = option.value
                for d in command._change_parameter():
                    if not d["name"] in kwargs:
                        kwargs[d["name"]] = None
                    else:
                        if d["type"] == 4:
                            kwargs[d["name"]] = int(kwargs[d["name"]])
                        elif d["type"] == 6:
                            kwargs[d["name"]] = await self.fetch_user(kwargs[d["name"]])
                if hasattr(command, "cog"):
                    return await command.callback(command.cog, interaction, **kwargs)
                else:
                    return await command.callback(interaction, **kwargs)

    async def _wait_response(self, interaction: Interaction, command: Command) -> None:
        await interaction.request.conn_info.ctx._wait_response.wait()
        command.dispatch(interaction)

    def slash_command(self, name: str, description: str):
        def decorator(coro):
            cmd = Command(coro, name, description)
            self.commands.append(cmd)
            return cmd
        return decorator

    def add_cog(self, cog) -> None:
        self.cogs[cog.__class__.__name__] = cog
        cog._inject(self)

    def remove_cog(self, name: str) -> None:
        cog = self.cogs[name]
        cog._rinject(self)
        del self.cogs[name]

    def load_extension(self, name: str) -> None:
        lib = import_module(name)
        lib.setup(self)

    def add_commandgroup(self, group):
        pass
        # self.commands.append(group)

    async def on_interaction(self, interaction: Interaction):
        if interaction.type == 2:
            return await self.process_slash_command(interaction.command.name, interaction)

    async def start(self, loop) -> None:
        self.loop = loop
        datas = await self.request("GET", "/applications/829578365634740225/commands")
        need = []
        need_edit = []
        for command in self.commands:
            if len(datas) == 0:
                need.append(command)
                continue
            for data in datas:
                if data["name"] == command.name:
                    if data["description"] == command.description:
                        for option in command.options:
                            if len(command.options) != len(data["options"]):
                                print('数が揃わない')
                                d = command.to_dict()
                                del d["name"]
                                del d["description"]
                                del d["type"]
                                need_edit.append((data["id"], d))
                            for api_option in data["options"]:
                                if option["name"] == api_option["name"]:
                                    if option["description"] == api_option["description"]:
                                        break
                                    else:
                                        d = command.to_dict()
                                        del d["name"]
                                        del d["description"]
                                        del d["type"]
                                        need_edit.append((data["id"], d))
                    else:
                        d = command.to_dict()
                        del d["name"]
                        del d["type"]
                        del d["options"]
                        need_edit.append((data["id"], d))
                        break
            else:
                need.append(command)
        for cmd in need:
            await self.request("POST", "/applications/829578365634740225/commands", json=cmd.to_dict())
        for cmd_id, data in need_edit:
            await self.request("PATCH", f"/applications/829578365634740225/commands/{cmd_id}", json=data)

    async def interaction(self, request):
        verify_key = VerifyKey(bytes.fromhex(self.publickey))
        signature = request.headers.get("x-signature-ed25519")
        timestamp = request.headers.get("x-signature-timestamp")
        try:
            verify_key.verify(f'{timestamp}{request.body.decode()}'.encode(), bytes.fromhex(signature))
        except BadSignatureError:
            return text("invalid request signature", status=401)
        else:
            data = request.json
            if data["type"] == 1:
                return json({"type": 1})
            else:
                interaction = Interaction(self, data)
                interaction.request = request
                return await self.on_interaction(interaction)

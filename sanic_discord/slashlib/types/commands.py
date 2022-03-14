from sanic.response import json
from inspect import signature
import asyncio
from .user import User

class Command:
    def __init__(self, coro, name, description):
        self.name = name
        self.description = description
        self.callback = coro
        self._after = []

    async def __call__(self, *args, **kwargs):
        return await self.callback(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        for f in self._after:
            if hasattr(self, "cog"):
                asyncio.create_task(f(self.cog, *args, **kwargs))
            else:
                asyncio.create_task(f(*args, **kwargs))

    def after(self, coro):
        self._after.append(coro)
        return coro

    def _change_parameter(self):
        rdata = []
        for p in signature(self.callback).parameters.values():
            if p.name in ["self", "interaction"]:
                continue
            if p.default != p.empty:
                data = p.default.payload
            else:
                data = CommandOption(p.name, "...").payload
            if p.annotation == p.empty:
                data["type"] = 3
            elif p.annotation == str:
                data["type"] = 3
            elif p.annotation == int:
                data["type"] = 4
            elif p.annotation == User:
                data["type"] = 6
            else:
                data["type"] = 3
            data["name"] = p.name
            rdata.append(data)
        return rdata

    @property
    def options(self):
        return self._change_parameter()

    def to_dict(self):
        payload = {
            "name": self.name,
            "description": self.description,
            "type": 1
        }
        options = self._change_parameter()
        if len(options) != 0:
            payload["options"] = options
        else:
            payload["options"] = []
        return payload

class CommandGroup:
    def __init__(self, name):
        self._name = name
        self._command = []

    @property
    def name(self):
        return self._name

    def slash_command(self, name, description):
        def decorator(coro):
            cmd = Command(coro, name, description)
            self._command.append(cmd)
            return cmd
        return decorator

    def to_dict(self):
        payload = {
            "name": self.name,
            "options": [command.to_dict() for command in self._command],
            "type": 1
        }
        return payload

class CommandOption:
    def __init__(self, description: str, required: bool=True):
        self.payload = {}
        self.payload["description"] = description
        self.payload["required"] = required

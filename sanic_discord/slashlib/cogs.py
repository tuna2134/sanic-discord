from inspect import getmembers
from .types.commands import Command

def slash_command(name, description):
    def decorator(coro):
        cmd = Command(coro, name, description)
        cmd._slash_command = True
        return cmd
    return decorator

def route(*args, **kwargs):
    def decorator(coro):
        coro._kwargs = kwargs
        coro._args = args
        coro._route = True
        return coro
    return decorator

class Cog:
    def _inject(self, bot):
        for name, func in getmembers(self):
            if hasattr(func, "_slash_command"):
                func.cog = self
                bot.commands.append(func)
            elif hasattr(func, "_route"):
                bot.web.add_route(func, *func._args, **func._kwargs)

    def _rinject(self, bot):
        for name, func in getmembers(self):
            if hasattr(func, "_slash_command"):
                bot.commands.remove(func)

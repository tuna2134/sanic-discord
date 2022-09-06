from sanic import response

from typing import TypedDict


class InteractionType(TypedDict):
    id: int
    application_id: int

class Interaction:
    def __init__(self, data: InteractionType):
        pass

import pytest

from sanic import Sanic, response
from sanic_testing import TestManager
from sanic_discord import Oauth2

from os import getenv


@pytest.fixture
def app():
    sanic_app = Sanic(__name__)
    oauth2 = Oauth2(
        sanic_app, client_id=getenv("CLIENT_ID"), client_secret=getenv("CLIENT_SECRET"),
        redirect_uri="http://localhost:8000"
    )
    TestManager(sanic_app)

    @sanic_app.get("/")
    def basic(request):
        return response.text("foo")

    return sanic_app

@pytest.mark.asyncio
async def test_basic_asgi_client(app):
    request, response = await app.asgi_client.get("/")

    assert response.body == b"foo"
    assert response.status == 200
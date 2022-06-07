from httpx import AsyncClient


class HttpClient:
    ApiUrl: str = "https://discord.com/api/v10"
    def __init__(self):
        self.session = httpClient()
        
    async def request(self, method: str, path: str, *args, **kwargs):
        kwargs["headers"] = {
            "Authorization": f"Bot {self.token}"
        }
        response = await self.session.request(method, self.ApiUrl + path, **kwargs)
        while True:
            if response.status_code == 404:
                raise NotFound("Not found error")
            elif response.status_code == 401:
                raise Unauthorized("Unauthorized error")
            elif response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                if response.headers.get("Retry-After"):
                    await asyncio.sleep(int(r.headers["Retry-After"]))
                else:
                    raise RateLimit("You did too many access.")
            elif response.status_code == 500:
                raise InternalServerError("500 Error")
                
    async def login(self, token: str) -> ClientUser:
        self.token = token
        self.user = await self.request("GET", "/users/@me")
        self.application_id = self.user["id"]
        return self.user

    async def fetchAppCommand(self) -> dict:
        return await self.request("GET", f"/applications/{self.application_id}/commands")
    
    async def addAppCommand(self, data: dict) -> dict:
        return await self.request("POST", f"/applications/{self.application_id}/commands", json=data)
    
    async def deleteAddCommand(self, command_id: int) -> dict:
        return await self.request("DELETE", f"/applications/{self.application_id}/commands/{command_id}")
    
    async def bulk_overwrite_app_commands(self, payload: List[dict]) -> List[dict]:
        return await self.request("PUT", f"/applications/{self.application_id}/commands", json=payload)

    async def responseInteraction(self, interactionid: int, token: str, data) -> dict:
        return await self.request("POST", f"/interactions/{interactionid}/{token}/callback", json=data

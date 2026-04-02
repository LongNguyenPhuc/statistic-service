from fastapi import APIRouter as Router
from jwt import encode
from ..middlewares.response import send_ok
from ..services.settings import get_settings
from pydantic import BaseModel
from ..providers.base import BaseProvider


class Controller:
    class Client(BaseModel):
        client: str

    def __init__(self, router: Router):
        self.provider = BaseProvider()

        @router.post("/generateClientKeys")
        async def client_key_generator(body: self.Client):
            return await self.generate_client_keys(body)

    async def generate_client_keys(self, body: Client):
        try:
            settings = get_settings()
            await self.provider.db.create_collection(body.client)
        except Exception as ex:
            pass

        return send_ok(
            {
                "token": encode(
                    {"client": body.client},
                    settings.SECRET_KEY,
                    algorithm="HS256",
                )
            }
        )

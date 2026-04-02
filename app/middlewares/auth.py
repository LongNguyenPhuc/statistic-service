from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode
from fastapi import Request, HTTPException
from ..services.db import get_db
from ..services.settings import get_settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            payload = await self.verify_jwt(credentials.credentials)

            if not payload:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return payload["client"]
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def verify_jwt(self, jwtoken: str) -> bool:
        try:
            settings = get_settings()

            payload = decode(
                jwtoken,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

            if payload["client"] not in await get_db().list_collection_names():
                raise Exception

            return payload
        except:
            return None

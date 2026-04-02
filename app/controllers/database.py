from app.middlewares.response import send_ok
from app.providers.database import DatabaseProvider
from app.services.mongo_query import QueryMiddleware
from typing import Annotated
from fastapi import APIRouter as Router, Depends, UploadFile, Body
from app.middlewares.auth import JWTBearer
from dateutil.parser import *


class Controller:
    def __init__(self, router: Router):
        self.database_provider = DatabaseProvider()

        @router.get("/collectionHeads")
        async def get_collection_column_head(
            collection: Annotated[str, Depends(JWTBearer())],
        ):
            return await self.collection_heads(collection)

        @router.post("/addData")
        async def addData(
            collection: Annotated[str, Depends(JWTBearer())],
            body: Annotated[list, Body()],
            dateField: str,
        ):
            def map_func(bodyVal):
                bodyVal[dateField] = parse(bodyVal[dateField])
                return bodyVal

            mappedBody = list(map(map_func, body))
            return await self.add_data(collection, mappedBody)

        @router.post("/importData")
        async def import_data_by_file(
            collection: Annotated[str, Depends(JWTBearer())],
            file: UploadFile,
            reset: bool | None = False,
        ):
            return await self.import_data(collection, file, reset)

        @router.put("/updateData")
        async def update_data_in_collection(
            collection: Annotated[str, Depends(JWTBearer())],
            query: Annotated[QueryMiddleware, Depends()],
            body: Annotated[object, Body()],
        ):
            return await self.update_data(collection, query, body)

        @router.delete("/deleteData")
        async def delete_data_from_collection(
            collection: Annotated[str, Depends(JWTBearer())],
            query: Annotated[QueryMiddleware, Depends()],
        ):
            return await self.delete_data(collection, query)

    async def add_data(self, collection: str, body: list):
        try:
            result = await self.database_provider.post(collection, body)

            return send_ok(result, "Success")
        except Exception as ex:
            return str(ex)

    async def import_data(self, collection: str, upload_file: UploadFile, reset: bool):
        try:
            result = await self.database_provider.import_file(
                collection, upload_file.file, reset
            )
            return send_ok(result, "Success")
        except Exception as ex:
            return str(ex)

    async def update_data(self, collection: str, query: QueryMiddleware, body: object):
        try:
            result = await self.database_provider.put(collection, body, query.filter)

            return send_ok(result, "ok")
        except Exception as ex:
            return str(ex)

    async def collection_heads(self, collection: str):
        try:
            result = await self.database_provider.get_heads(collection)

            return send_ok(result, "ok")
        except Exception as ex:
            return str(ex)

    async def delete_data(self, collection: str, query: QueryMiddleware):
        try:
            result = await self.database_provider.delete(collection, query.filter)

            return send_ok(result, "ok")
        except Exception as ex:
            return str(ex)

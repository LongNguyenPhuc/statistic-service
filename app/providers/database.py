from json import load, loads
from bson.json_util import dumps
from app.providers.base import BaseProvider
from app.services.db import get_pymongo_client
from datetime import datetime
from asyncio import gather
from typing import BinaryIO
from pymongo_schema.extract import extract_pymongo_client_schema
from ..services.settings import get_settings


class DatabaseProvider(BaseProvider):
    def __init__(self) -> None:
        pass

    async def import_file(self, collection: str, file: BinaryIO, reset=False):
        async def convert_date_column_type(data):
            async def check_key_and_convert(key):
                if data[key] is not None:
                    # Format date string to date
                    data[key] = datetime.strptime(
                        data[key] + "00",
                        (
                            "%Y-%m-%d %H:%M:%S.%f%z"
                            if "." in data[key]
                            else "%Y-%m-%d %H:%M:%S%z"
                        ),
                    )

            keys = list(data.keys())

            gather(
                *map(check_key_and_convert, list(filter(lambda k: "Date" in k, keys)))
            )

        try:
            if reset:  # Reset database
                await self.delete(collection)

            body = load(file)

            await gather(*map(convert_date_column_type, body))

            result = await self.post(collection, body)

            return loads(dumps(result))
        except Exception as ex:
            raise ex

    async def get_heads(self, collection: str):
        client = get_pymongo_client()
        settings = get_settings()
        schema = extract_pymongo_client_schema(
            client, [settings.DATABASE["DBNAME"]], [collection]
        )

        return [*schema[settings.DATABASE["DBNAME"]][collection]["object"].keys()]

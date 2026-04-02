from app.services.db import get_db
from bson.json_util import dumps
from json import loads
from motor.core import AgnosticDatabase as Database


class BaseProvider(object):
    db: Database = get_db()

    def __init__(self) -> None:
        pass

    async def get(self, collection, filter={}, attributes={"_id": False}) -> list:
        try:
            cursor = self.db[collection].find(filter=filter, projection=attributes)
            return list([val async for val in cursor])
        except Exception as ex:
            raise ex

    async def post(self, collection, body) -> list:
        try:
            result = await self.db[collection].insert_many(body)
            return loads(dumps(result.inserted_ids))
        except Exception as ex:
            raise ex

    async def put(self, collection, body, where={}) -> int:
        try:
            result = await self.db[collection].update_many(where, {"$set": body})
            return result.modified_count
        except Exception as ex:
            raise ex

    async def delete(self, collection, where={}) -> int:
        try:
            result = await self.db[collection].delete_many(where)
            return result.deleted_count
        except Exception as ex:
            raise ex

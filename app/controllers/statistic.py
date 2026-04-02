from app.middlewares.auth import JWTBearer
from app.services.mongo_query import QueryMiddleware
from app.providers.statistic import StatisticProvider
from app.middlewares.response import send_ok
from fastapi import APIRouter as Router, Depends
from typing import Annotated


class Controller:
    def __init__(self, router: Router):
        self.statistic_provider = StatisticProvider()

        @router.get("")
        # @token_required
        # @middleware
        async def get_group_statistic(
            collection: Annotated[str, Depends(JWTBearer())],
            query: Annotated[QueryMiddleware, Depends()],
            groupBy: str,
            countBy: str,
        ):
            return await self.get_statistic(collection, query, groupBy, countBy)

        @router.get("/overtime")
        # @token_required
        # @middleware
        async def get_group_statistic_over_time(
            collection: Annotated[str, Depends(JWTBearer())],
            query: Annotated[QueryMiddleware, Depends()],
            groupBy: str,
            countBy: str,
            dateField: str,
            dateFreq: str | None = None,
            dateInterval: str | None = None,
        ):
            return await self.get_statistic_over_time(
                collection, query, groupBy, countBy, dateField, dateFreq, dateInterval
            )

    async def get_statistic(
        self, collection: str, query: QueryMiddleware, groupBy: str, countBy: str
    ):
        try:
            # payload should include:
            #   - filters
            #   - group_by
            #   - count_by
            payload = {
                "group_by": groupBy.split(","),
                "count_by": countBy.split(","),
                "filter": query.filter,
                "attributes": {"_id": False},
            }

            payload["attributes"] |= {
                col: 1 for col in (payload["count_by"] + payload["group_by"])
            }
            result = await self.statistic_provider.get_count(collection, payload)
            
            return send_ok(result, "Successfully get statistic")
        except Exception as ex:
            return str(ex)

    async def get_statistic_over_time(
        self,
        collection: str,
        query: QueryMiddleware,
        groupBy: str,
        countBy: str,
        dateField: str,
        dateFreq: str | None = None,
        dateInterval: str | None = None,
    ):
        # payload should include:
        #   - filters
        #   - group_by
        #   - count_by
        dict_freq = [
            {"label": "hour", "code": "H"},
            {"label": "day", "code": "D"},
            {"label": "month", "code": "M"},
        ]

        try:
            payload = {
                "group_by": groupBy.split(","),
                "count_by": countBy.split(","),
                "filter": query.filter,
                "date_field": dateField,
                "date_freq": "H",
                "date_query": "H",
                "attributes": {dateField: 1, "_id": False},
            }

            if dateFreq:
                for freq in dict_freq:
                    if freq["label"] == dateFreq:
                        payload["date_freq"] = freq["code"]
                        payload["date_query"] = (str(dateInterval) or "") + freq["code"]
                        break

            payload["attributes"] |= {
                col: 1 for col in (payload["count_by"] + payload["group_by"])
            }

            result = await self.statistic_provider.get_count_overtime(
                collection, payload
            )
            return send_ok(result, "Successfully query statistic")
        except Exception as ex:
            return str(ex)

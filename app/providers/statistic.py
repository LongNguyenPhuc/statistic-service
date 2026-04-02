from fastapi.routing import json
from pandas import DataFrame, Grouper
from operator import itemgetter
from app.providers.base import BaseProvider


class StatisticProvider(BaseProvider):
    def __init__(self) -> None:
        pass

    async def get_count(self, collection, payload) -> list:
        # payload should include:
        #   - filter
        #   - group_by
        #   - count_by
        #   - attributes

        try:
            count_by, group_by, filter, attributes = itemgetter(
                "count_by", "group_by", "filter", "attributes"
            )(payload)

            datas = await self.get(collection, filter, attributes)

            return (
                json.loads(
                    DataFrame(datas)
                    .groupby(group_by)[count_by]
                    .nunique()
                    .to_json(orient="table")
                )["data"]
                if len(datas) > 0
                else []
            )

        except Exception as e:
            raise e

    async def get_count_overtime(self, collection, payload):
        try:
            (
                count_by,
                group_by,
                filter,
                attributes,
                date_field,
                date_freq,
                date_query,
            ) = itemgetter(
                "count_by",
                "group_by",
                "filter",
                "attributes",
                "date_field",
                "date_freq",
                "date_query",
            )(
                payload
            )

            datas = await self.get(collection, filter, attributes)
            if len(datas) == 0:
                return []

            base_group_by = group_by.copy()
            base_group_by.append(Grouper(key=date_field, freq=date_query))

            return json.loads(
                DataFrame(DataFrame(datas).groupby(base_group_by)[count_by].nunique())
                # Pad in no data
                .reset_index()
                .set_index(date_field)
                .groupby(group_by)[count_by]
                .resample(date_freq)
                .asfreq()
                .fillna(0)
                .to_json(orient="table")
            )["data"]
        except Exception as e:
            raise e

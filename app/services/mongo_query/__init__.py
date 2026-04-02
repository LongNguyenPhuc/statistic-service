from functools import wraps
from app.services.mongo_query.middle import modify_filter_string


class QueryMiddleware:
    def __init__(self, filter: str | None = None):
        self.raw_filter = filter
        self.filter = modify_filter_string(filter) if filter is not None else {}
        return

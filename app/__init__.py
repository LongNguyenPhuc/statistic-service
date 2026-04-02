from fastapi import FastAPI
from .controllers import init_routes
from .services.db import get_db


def create_app():
    app = FastAPI()
    init_routes(app)
    return app

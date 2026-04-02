import os
from fastapi import FastAPI, APIRouter as Router


def init_routes(app: FastAPI):
    print("----------------------------------------")
    print("            SERVER ROUTING              ")
    for module in os.listdir(os.path.dirname(__file__)):
        # Skip this file
        if module == "__init__.py" or module[-3:] != ".py":
            continue

        # Dynamically import the routes
        route_name = module[:-3]
        import_module = __import__(f"app.controllers.{route_name}", fromlist=[""])
        router = Router(prefix=f"/{route_name}", tags=[route_name.capitalize()])
        import_module.Controller(router)
        app.include_router(router)
        print(f" /{route_name}")
    del module
    print("----------------------------------------")

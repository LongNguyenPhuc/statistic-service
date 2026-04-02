from app.utils.templates import response_template
from fastapi.responses import JSONResponse


def send_ok(data, message=""):
    return JSONResponse(response_template(data, message))

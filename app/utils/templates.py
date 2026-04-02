from datetime import datetime


def response_template(data, message="", violations=None):
    return {
        "message": message,
        "data": data,
        "success": violations is None,
        "timestamp": datetime.now().astimezone().isoformat(),
        "violations": violations or None,
    }

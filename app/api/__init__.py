from middleware.log import logger
from config import get_apirouters_data
from serialization import res
from server import get_server_data

__all__ = ["logger", "get_server_data", "get_apirouters_data", "res"]


def get_apirouter_list():
    from .models import model_router
    from .test import test_router
    return [model_router, test_router]
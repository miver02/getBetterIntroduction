from middleware.log import logger
from config import get_apirouters_data

__all__ = ["logger", "get_apirouters_data"]

# 不立即实例化，而是定义工厂函数
def create_server_data():
    from .files import HandleFiles
    from .model import ConnModel
    from .routers import Routers
    return {
        "hf": HandleFiles(),
        "cm": ConnModel(),
        "rts": Routers()
    }

# 使用延迟初始化
server_data = None

def get_server_data():
    global server_data
    if server_data is None:
        server_data = create_server_data()
    return server_data
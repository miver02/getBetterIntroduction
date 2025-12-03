from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
from middleware import logger, add_cors_middleware
from api import get_apirouter_list
from dotenv import load_dotenv


# 加载环境变量
load_dotenv(".env")
app = FastAPI(title="简历分析系统", version="1.0.0")

# 注册中间件
add_cors_middleware(app)

# 注册路由
for router in get_apirouter_list():
    app.include_router(router)


if __name__ == '__main__':
    logger.info("启动服务...")
    uvicorn.run("main:app", host="0.0.0.0", port=6666, reload=True)
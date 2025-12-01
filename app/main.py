from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
from middleware.log import logger
from api import get_apirouter_list
from dotenv import load_dotenv


# 加载环境变量
load_dotenv(".env")
app = FastAPI(title="简历分析系统", version="1.0.0")

# 注册路由
for router in get_apirouter_list():
    app.include_router(router)

@app.get("/")
async def main():
    return FileResponse("index.html")


if __name__ == '__main__':
    logger.info("启动服务...")
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
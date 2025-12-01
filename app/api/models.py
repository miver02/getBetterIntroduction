from typing import List
from fastapi import APIRouter, File, Form, UploadFile
from . import logger, get_apirouters_data, res, get_server_data


MODELS_ROUTES = get_apirouters_data().get("MODELS_ROUTES")

model_router = APIRouter(
    prefix=MODELS_ROUTES["prefix"],
    tags=MODELS_ROUTES["tags"],
)

get_rank_data = MODELS_ROUTES["endpoints"].get("get_rank")

@model_router.post(get_rank_data["path"], summary=get_rank_data["summary"], description=get_rank_data["description"])
async def get_rank(
    job: str = Form(...),  # 从表单获取职位名称
    select: str = Form(...),  # 从表单获取筛选条件
    files: List[UploadFile] = File([]),  # 可选的简历文件
):
    logger.info(f"处理POST请求，职位: {job}, 筛选条件: {select}")
    logger.info(f"收到的文件数量: {len(files) if files else 0}")

    # 创建实例
    hf = get_server_data().get("hf")
    cm = get_server_data().get("cm")

    # 确保临时文件夹存在
    err = await hf.if_exist_files()
    if err is not None:
        return res.ErrorResponse(code=500, message=str(err))
    # 处理上传的文件
    err = await hf.handle_files(files)
    if err is not None:
        return res.ErrorResponse(code=500, message=str(err))

    # 读取PDF内容
    pdf_contents = await hf.read_pdf()
    
    # 调用AI分析
    logger.info(f"模型格式化数据中...")
    response, err = await cm.conn_ai(pdf_contents, job, select)
    if err is not None:
        return res.ErrorResponse(code=500, message=str(err))
    return res.SuccessResponse(data=response)
    



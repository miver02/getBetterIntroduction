import os
from typing import List, Optional
from fastapi import FastAPI, File, Form, Query, UploadFile
from fastapi.responses import FileResponse
from openai import OpenAI
import uvicorn
import logging
from basecode import HandleFiles, ConnDeepseek

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


async def save_uploaded_file(file, relative_path, pdf_paths):
    # 保存文件
    try:
        # 读取上传的文件内容
        content = await file.read()
        # 写入到目标文件
        with open(relative_path, "wb") as f:
            f.write(content)
        logger.info(f"保存文件: {relative_path}")
    except Exception as e:
        logger.error(f"保存文件 {file.filename} 时出错: {e}")


@app.post("/get_job/better_rank")
async def get_better_intro(
    job: str = Form(...),  # 从表单获取职位名称
    select: str = Form(...),  # 从表单获取筛选条件
    files: List[UploadFile] = File([]),  # 可选的简历文件
    folder: List[UploadFile] = File([])  # 可选的文件夹中的文件
):
    logger.info(f"处理POST请求，职位: {job}, 筛选条件: {select}")
    logger.info(f"收到的文件数量: {len(files) if files else 0}")
    logger.info(f"收到的文件夹文件数量: {len(folder) if folder else 0}")
    
    # 创建文件处理器实例
    hf = HandleFiles()
    pdf_paths = []  # 存储PDF文件相对路径的列表
    
    # 确保临时文件夹存在
    pdf_dir = "./pdf"
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    else:
        # 清空临时文件夹（可选，取决于您的需求）
        for filename in os.listdir(pdf_dir):
            file_path = os.path.join(pdf_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger.error(f"清理文件时出错: {e}")
    
    # 处理上传的文件
    if files:
        logger.info(f"收到 {len(files)} 个文件")
        for file in files:
            if file.filename.lower().endswith('.pdf'):
                # 构建保存路径
                relative_path = pdf_dir + '/' + file.filename
                
                await save_uploaded_file(file, relative_path, pdf_paths)
                # 添加到路径列表
                pdf_paths.append(relative_path)
    # 处理文件夹中的文件
    if folder:
        logger.info(f"收到 {len(folder)} 个文件夹文件")
        for file in folder:
            if file.filename.lower().endswith('.pdf'):
                # 从文件夹路径中提取文件名
                # 文件夹上传时，filename通常包含路径，如 "subfolder/file.pdf"
                _, filename = os.path.split(file.filename)
                relative_path = pdf_dir + '/' + filename
                
                await save_uploaded_file(file, relative_path, pdf_paths)
                # 添加到路径列表
                pdf_paths.append(relative_path)

    # 读取PDF内容
    pdf_contents = await hf.read_pdf(pdf_paths)
    
    # 调用AI分析
    cds = ConnDeepseek()
    logger.info(f"模型格式化数据中...")
    response = cds.conn_ai(pdf_contents, job, select)
    if response:
        return {"status": "success", "data": response}
    else:
        return {"status": "false", "data": response}

@app.get("/")
async def main():
    return FileResponse("index.html")

if __name__ == '__main__':
    logger.info("启动服务...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
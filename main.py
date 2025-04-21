import json
import os
import asyncio
from fastapi import FastAPI, Query
from openai import OpenAI
import uvicorn
import PyPDF2
import re
import logging


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class HandleFiles:
    def __init__(self):
        self.relative_paths = []
        self.font_by_pdfs = []

    def get_pdf_path(self,folder_path='./pdf'):
        """
        获取指定文件夹下所有文件的相对路径
        """
        try:
            for root, dirs, files in os.walk(folder_path):
                for filename in files:
                    relative_path = os.path.join(folder_path, filename)
                    self.relative_paths.append(relative_path)

            logger.info(f"文件路径如下:{self.relative_paths}")
        except Exception as e:
            logger.error(f"获取文件路径错误：{e}")
        
    async def get_fonts_with_pypdf(self, pdf_path):
        """
        使用pypdf获取字体资源信息
        """
        try:
            font_by_page = {}
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                # 遍历每一页
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text.split():
                        font_by_page[f"第{page_num}页"] = text
                        
                self.font_by_pdfs.append(font_by_page)                                                          
        except Exception as e:
            logger.error(f"获取{pdf_path}文件内容错误: {e}")
    async def read_pdf(self):
        """
        读取pdf文件
        """
        try:
            tasks = []
            for pdf_path in self.relative_paths:
                task = asyncio.create_task(self.get_fonts_with_pypdf(pdf_path))
                tasks.append(task)
            await asyncio.gather(*tasks)    

            logger.info(f"文件内容读取完毕")
        except Exception as e:
            logger.error(f"任务列表处理任务出现错误: {e}")

class ConnDeepseek:
    def __init__(self):
        self.api_key = os.environ.get('DEEPSEEK_V3')

    def conn_ai(self, pdf_contents, job):
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )

            completion = client.chat.completions.create(
                extra_headers={},
                extra_body={},
                model="deepseek/deepseek-v3-base:free",
                messages=[
                    {
                    "role": "user",
                    "content": f"我公司需要招聘{job}.读取{pdf_contents},帮我整理文件,并将数据格式化,一份简历封装为一个json数据,\
                        json数据的键包含姓名,性别,年龄,工龄,工作经历,项目经历,json数据的值需要你从{pdf_contents}中提取或者总结,将所有简历整理为json数据后,按照所需岗位排序后返回给我json列表"
                    }
                ]
            )

            content = completion.choices[0].message.content
            match = re.search(r'\[(.*?)\]', content)
            if match:
                result = match.group(1)
                logger.info(f"ai整理文档成功,返回数据: {result}")
                result_json = json.loads(result)
                return result_json
        except Exception as e:
            logger.error(f"ai整理文档错误: {e}")


hf = None
    

@app.on_event("startup")
async def startup_event():
    global hf
    hf = HandleFiles()
    logger.info("获取pdf文件的相对路径...")
    hf.get_pdf_path()

    logger.info("读取文件信息...")
    await hf.read_pdf()


@app.get("/get_job/better_rank")
async def main(job: str = Query(..., description="招聘岗位")):
    global hf
    cds = ConnDeepseek()    
    logger.info(f"模型格式化数据中...")
    response = cds.conn_ai(hf.font_by_pdfs, job)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
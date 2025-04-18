import os
import asyncio
from fastapi import FastAPI
from openai import OpenAI
import uvicorn
import PyPDF2
import os
import logging


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class HandleFiles:
    def __init__(self):
        self.relative_paths = []
        self.font_by_pdfs = []
        self.read_results = None

    def get_pdf_path(self,folder_path='./pdf'):
        """
        获取指定文件夹下所有文件的相对路径
        """
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                relative_path = os.path.join(folder_path, filename)
                self.relative_paths.append(relative_path)
        
    async def get_fonts_with_pypdf(self, pdf_path):
        """
        使用pypdf获取字体资源信息
        """
        font_by_page = {}
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            # 遍历每一页
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text.split():
                    font_by_page[f"第{page_num}页"] = text
                    
            self.font_by_pdfs.append(font_by_page)

    async def read_pdf(self):
        """
        读取pdf文件
        """
        tasks = []
        for pdf_path in self.relative_paths:
            task = asyncio.create_task(self.get_fonts_with_pypdf(pdf_path))
            tasks.append(task)
        await asyncio.gather(*tasks)


class ConnDeepseek:
    def __init__(self):
        self.api_key = os.environ.get('DEEPSEEK_V3')

    def conn_ai(self):
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            extra_body={},
            model="deepseek/deepseek-v3-base:free",
            messages=[
                {
                "role": "user",
                "content": "What is the meaning of life?"
                }
            ]
        )
        print(completion.choices[0].message.content)
    



async def main():
    """hf = HandleFiles()
    logger.info("获取pdf文件的相对路径...")
    hf.get_pdf_path()
    logger.info(f"文件路径如下:{hf.relative_paths}")

    logger.info("读取文件信息...")
    await hf.read_pdf()
    logger.info(f"文件信息如下:{hf.font_by_pdfs}")"""

    cd = ConnDeepseek()    
    


if __name__ == '__main__':
    asyncio.run(main())
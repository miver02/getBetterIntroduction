import asyncio
import os
import PyPDF2
from . import logger


class HandleFiles:
    """处理pdf文件"""
    def __init__(self):
        self.pdf_paths = []
        self.font_by_pdfs = []
        self.pdf_dir = "./pdf"

    async def if_exist_files(self) -> str:
        """确保临时文件夹存在"""
        try:
            if not os.path.exists(self.pdf_dir):
                os.makedirs(self.pdf_dir)
            else:
                # 清空临时文件夹（可选，取决于您的需求）
                for filename in os.listdir(self.pdf_dir):
                    file_path = os.path.join(self.pdf_dir, filename)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        logger.error(f"清理文件时出错: {e}")
                        return str(e)
            return None
        except Exception as e:
            logger.error(f"确保临时文件夹存在时出错: {e}")
            return str(e)

    async def save_uploaded_file(self, file, relative_path) -> str | None:
        """保存文件"""
        try:
            # 读取上传的文件内容
            content = await file.read()
            # 写入到目标文件
            with open(relative_path, "wb") as f:
                f.write(content)
            logger.info(f"保存文件: {relative_path}")
        except Exception as e:
            logger.error(f"保存文件 {file.filename} 时出错: {e}")
            return str(e)

    async def handle_files(self, files) -> str:
        """处理文件"""
        try:
            if files:
                logger.info(f"收到 {len(files)} 个文件")
            else:
                logger.info("没有收到文件")
                return "没有收到文件"
            for file in files:
                # 跳过非PDF文件
                if not file.filename.lower().endswith('.pdf'):
                    continue
                
                # 安全拼接路径
                _, filename = os.path.split(file.filename)
                relative_path = os.path.join(self.pdf_dir, filename)  # 跨平台兼容
                
                # 保存文件
                await self.save_uploaded_file(file, relative_path)
                self.pdf_paths.append(relative_path)
            return None
        except Exception as e:
            logger.error(f"保存文件 {file.filename} 时出错: {e}")
            return str(e)
    
    async def get_fonts_with_pypdf(self, pdf_path):
        """使用pypdf获取字体资源信息"""
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
        """读取pdf文件"""
        try:
            tasks = []
            for pdf_path in self.pdf_paths:
                task = asyncio.create_task(self.get_fonts_with_pypdf(pdf_path))
                tasks.append(task)

            await asyncio.gather(*tasks)  
            logger.info(f"文件内容读取完毕")
            return self.font_by_pdfs
        except Exception as e:
            logger.error(f"任务列表处理任务出现错误: {e}")
            return None
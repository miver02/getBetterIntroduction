import asyncio
from io import BytesIO
import warnings
import pdfplumber
from . import logger


# 更准确地匹配警告消息
warnings.filterwarnings("ignore", message=".*Could get FontBBox from font descriptor.*")
warnings.filterwarnings("ignore", message=".*Cannot set gray.*")
# 直接忽略所有pdfminer的警告
warnings.filterwarnings("ignore", category=UserWarning, module="pdfminer")

class HandleFiles:
    """处理pdf文件"""
    def __init__(self):
        self.pdf_files = []     # 存储pdf文件
        self.font_by_pdfs = []  # 存储pdf文件中的字体信息
    async def handle_files(self, files) -> str | None:
        """处理文件"""
        try:
            if files:
                logger.info(f"开始处理文件...")
            else:
                logger.info("没有收到文件")
                return "没有收到文件"
            
            self.pdf_files = [] 
            for file in files:
                # 跳过非PDF文件
                if not file.filename.lower().endswith('.pdf'):
                    continue
                
                # 读取文件内容并存储
                content = await file.read()
                self.pdf_files.append({
                    'filename': file.filename,
                    'content': content
                })
            return None
        except Exception as e:
            logger.error(f"处理文件 {file.filename} 时出错: {e}")
            return str(e)
    
    async def get_fonts_with_pypdf(self, pdf_file: dict):
        """使用pypdf获取字体资源信息"""
        try:
            text = ""
            # 使用BytesIO从内存中读取PDF内容
            pdf_content = BytesIO(pdf_file['content'])
            with pdfplumber.open(pdf_content) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

                # 如果没有提取到文本，尝试其他方法
                if not text.strip():
                    for page in pdf.pages:
                        # 尝试提取表格数据
                        tables = page.extract_tables()
                        for table in tables:
                            for row in table:
                                text += " ".join([str(cell) if cell else "" for cell in row]) + "\n"
                        
            self.font_by_pdfs.append(text)                                                          
        except Exception as e:
            logger.error(f"获取{pdf_file['filename']}文件内容错误: {e}")
            # 即使出错也添加空字符串，保证数组长度一致
            self.font_by_pdfs.append("")
    async def read_pdf(self) -> list | None:
        """读取pdf文件"""
        try:
            tasks = []
            self.font_by_pdfs = []
            
            for pdf_file in self.pdf_files:
                task = asyncio.create_task(self.get_fonts_with_pypdf(pdf_file))
                tasks.append(task)

            await asyncio.gather(*tasks)  
            logger.info(f"文件内容读取完毕")
            return self.font_by_pdfs
        except Exception as e:
            logger.error(f"任务列表处理任务出现错误: {e}")
            return None
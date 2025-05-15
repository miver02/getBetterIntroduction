
# 配置日志
import asyncio
import json
import logging
import os
import re
import PyPDF2
from openai import OpenAI


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HandleFiles:
    def __init__(self):
        self.relative_paths = []
        self.font_by_pdfs = []
        
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

    async def read_pdf(self, pdf_paths):
        """
        读取pdf文件
        """
        try:
            tasks = []
            for pdf_path in pdf_paths:
                task = asyncio.create_task(self.get_fonts_with_pypdf(pdf_path))
                tasks.append(task)

            await asyncio.gather(*tasks)  
            logger.info(f"文件内容读取完毕")
            return self.font_by_pdfs
        except Exception as e:
            logger.error(f"任务列表处理任务出现错误: {e}")
            return None


class ConnDeepseek:
    def __init__(self):
        self.api_key = os.environ.get('DEEPSEEK_V3')

    def extract_json_array(self, content):
        """
        从AI生成的文本中提取JSON数组，处理多种可能的格式问题
        """
        # 尝试多种提取方法
        
        # 方法1: 尝试从Markdown代码块中提取
        code_block_pattern = re.compile(r'```(?:json)?\s*\n([\s\S]*?)\n```', re.DOTALL)
        code_match = code_block_pattern.search(content)
        if code_match:
            try:
                json_text = code_match.group(1).strip()
                return json.loads(json_text)
            except json.JSONDecodeError:
                logger.debug("从代码块提取JSON失败，尝试其他方法")
        
        # 方法2: 尝试直接查找有效的JSON数组
        array_pattern = re.compile(r'\[\s*\{[\s\S]*?\}\s*\]', re.DOTALL)
        array_match = array_pattern.search(content)
        if array_match:
            try:
                return json.loads(array_match.group(0))
            except json.JSONDecodeError:
                logger.debug("从文本中提取JSON数组失败，尝试其他方法")
        
        # 方法3: 如果上述都失败，尝试到Extra data错误位置截断
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            error_str = str(e)
            if "Extra data" in error_str:
                try:
                    # 从错误信息中提取字符位置
                    char_pos = int(re.search(r'char (\d+)', error_str).group(1))
                    # 截取到该位置的字符串
                    truncated = content[:char_pos]
                    # 尝试解析截断后的内容
                    return json.loads(truncated)
                except (json.JSONDecodeError, AttributeError, ValueError) as sub_e:
                    logger.debug(f"截断JSON解析失败: {sub_e}")
        
        # 方法4: 修复常见JSON格式问题
        # 移除尾部逗号
        fixed_content = re.sub(r',(\s*[\]}])', r'\1', content)
        try:
            return json.loads(fixed_content)
        except json.JSONDecodeError:
            pass
        
        # 最后记录原始内容以便调试
        logger.error(f"无法解析JSON，原始内容前100字符: {content[:100]}...")
        return None

    def conn_ai(self, pdf_contents, job, select):
        prompt = f"""我公司需要招聘{job}。读取{pdf_contents},理解文件内容和细节,帮我整理文件,并将数据格式化。
                请严格按照以下要求返回：
                1. 一份简历封装为一个JSON对象
                2. 将所有简历JSON对象放在一个JSON数组中
                3. 返回格式必须是有效的JSON，不要添加任何额外文本或说明,JSON的键必须是英文,JSON的值必须是原文件中的总结或者原文
                4. JSON数组按照与岗位匹配度从高到低排序
                5. 注意以下字段提取细节:性别根据文件提取.
                6. 根据筛选条件{select}，按照职位符合度以及筛选条件符合度进行排序
                

                例如:
                ```json
                [
                {{"name": "张三", "gender": "男", "age": 30, "work_years": 5, "work_experience": "...", "project_experience": "..."}},
                {{"name": "李四", "gender": "女", "age": 28, "work_years": 3, "work_experience": "...", "project_experience": "..."}}
                ]
                ```

                请仅返回JSON数组，不要包含其他文本、注释或说明。
                """
        try:
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key,
            )
            
            completion = client.chat.completions.create(
                extra_headers={},
                extra_body={},
                model="deepseek/deepseek-chat-v3-0324",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个精确的JSON生成器。你只返回有效的JSON，不返回任何其他文本。你不在JSON中添加任何注释或解释。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            content = completion.choices[0].message.content
            result_json = self.extract_json_array(content)
            logger.info(f"json: {result_json}")
            return result_json
        except Exception as e:
            logger.error(f"ai整理文档错误: {e}")
            return None

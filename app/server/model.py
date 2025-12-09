import json
import os
import re
from typing import Tuple
import requests
from . import logger, MODEL_API_URL, MODEL_NAME


class ConnModel:
    """"link to model"""
    def __init__(self):
        self.api_key = os.environ.get('My_ALIBAILIAN_API_KEY')
        self.modelname = MODEL_NAME

    async def extract_json_array(self, content) -> Tuple[list, str]:
        """从AI生成的文本中提取JSON数组，处理多种可能的格式问题"""
        # 尝试多种提取方法
        
        # 方法1: 尝试从Markdown代码块中提取
        code_block_pattern = re.compile(r'```(?:json)?\s*\n([\s\S]*?)\n```', re.DOTALL)
        code_match = code_block_pattern.search(content)
        if code_match:
            try:
                json_text = code_match.group(1).strip()
                return json.loads(json_text), None
            except json.JSONDecodeError:
                logger.debug("从代码块提取JSON失败，尝试其他方法")
        
        # 方法2: 尝试直接查找有效的JSON数组
        array_pattern = re.compile(r'\[\s*\{[\s\S]*?\}\s*\]', re.DOTALL)
        array_match = array_pattern.search(content)
        if array_match:
            try:
                return json.loads(array_match.group(0)), None
            except json.JSONDecodeError:
                logger.debug("从文本中提取JSON数组失败，尝试其他方法")
        
        # 方法3: 如果上述都失败，尝试到Extra data错误位置截断
        try:
            return json.loads(content), None
        except json.JSONDecodeError as e:
            error_str = str(e)
            if "Extra data" in error_str:
                try:
                    # 从错误信息中提取字符位置
                    char_pos = int(re.search(r'char (\d+)', error_str).group(1))
                    # 截取到该位置的字符串
                    truncated = content[:char_pos]
                    # 尝试解析截断后的内容
                    return json.loads(truncated), None
                except (json.JSONDecodeError, AttributeError, ValueError) as sub_e:
                    logger.debug(f"截断JSON解析失败: {sub_e}")
        
        # 方法4: 修复常见JSON格式问题
        # 移除尾部逗号
        fixed_content = re.sub(r',(\s*[\]}])', r'\1', content)
        try:
            return json.loads(fixed_content), None
        except json.JSONDecodeError:
            pass        
        # 最后记录原始内容以便调试
        logger.error(f"无法解析JSON，原始内容前100字符: {content[:100]}...")
        return None, str("无法解析JSON")

    async def conn_ai(self, pdf_contents, job, select) -> Tuple[dict, str]:
        prompt = f"""我公司需要招聘{job}。读取{pdf_contents},理解文件内容和细节,帮我整理文件,并将数据格式化。
                请严格按照以下要求返回：
                1. 一份简历封装为一个JSON对象
                2. 将所有简历JSON对象放在一个JSON数组中
                3. 返回格式必须是有效的JSON，不要添加任何额外文本或说明,JSON的键必须是英文,JSON的值必须是原文件中的总结或者原文
                4. 根据筛选条件{select}，按照职位符合度以及筛选条件符合度进行排序
                5. JSON数组按照与岗位匹配度从高到低排序
                6. 注意以下字段提取细节:{{
                    name: 全文搜索并且判断应聘人的姓名,
                    age: 全文搜索并且判断应聘人的年龄, 如果没有直接显示年龄, 尝试根据出生日期,毕业年份和工作年限等信息推算年龄,
                    major: 全文搜索并且判断应聘人的专业,
                    phone: 全文搜索并且判断应聘人的手机号, 格式一定要统一为11位数字,
                
                    gender: 全文搜索并且判断应聘人的性别,
                    email: 全文搜索并且判断应聘人的邮箱,
                    address: 全文搜索并且判断应聘人的现居住地址,
                    work_years: 全文搜索并且判断应聘人的工作年限, 如果没有直接显示工作年限, 尝试根据工作经历或者项目经历的日期等信息推算工作年限,
                    skills: 全文搜索并且判断应聘人的技术技能,
                    work_experience: 全文搜索并且判断应聘人的工作经历或者实习经历,
                    project_experience: 全文搜索并且判断应聘人的项目经历,
        
                    education: 全文搜索并且判断应聘人的学历,
                    university: 全文搜索并且判断应聘人的毕业院校,
                    degree_time: 全文搜索并且判断应聘人的毕业时间,
                    competitions: 全文搜索并且判断应聘人的校园经历或者获奖经历,
                    self_introduction: 全文搜索并且判断应聘人的自我评价或者自我介绍,
                }}
                
                例如:
                ```json
                [
                {{"name": "张山", "age": 18, "major": "计算机科学与技术", "phone": "12345678901", "gender": "男", "email": "zhangsan@example.com", "address": "北京", "work_years": 5, "skills": ["Python", "Java"], 
                    "work_experience": ["百度", "阿里"], "project_experience": ["购物商城系统", "基于 YOLOV11 实现街景字符识别"], "education": "本科", "university": "清华大学", "degree_time": "2023年6月", 
                    "competitions": ["ACM国际大学生程序设计竞赛二等奖"], "self_introduction": "热爱编程，喜欢挑战自我。"}},
                {{"name": "李四", "age": 18, "major": "计算机科学与技术", "phone": "12345678901", "gender": "男", "email": "zhangsan@example.com", "address": "北京", "work_years": 5, "skills": ["Python", "Java"], 
                    "work_experience": ["百度", "阿里"], "project_experience": ["购物商城系统", "基于 YOLOV11 实现街景字符识别"], "education": "本科", "university": "清华大学", "degree_time": "2023年6月", 
                    "competitions": ["ACM国际大学生程序设计竞赛二等奖"], "self_introduction": "热爱编程，喜欢挑战自我。"}},
                ]
                ```

                请仅返回JSON数组，不要包含其他文本、注释或说明。
            """
        try:
            # 使用requests库直接调用API，避免OpenAI库的代理问题
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                # "model": "deepseek/deepseek-chat-v3-0324",
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个精确的JSON生成器。你只返回有效的JSON，不返回任何其他文本。你不在JSON中添加任何注释或解释。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                    # 可以定义结构化输出
                ],
                "stream": False,
                "response_format": {"type": "json_object"}
            }
            
            response = requests.post(
                MODEL_API_URL,
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                result_json, err = await self.extract_json_array(content)
                # logger.info(f"json: {result_json}")
                return result_json, err
            else:
                logger.error(f"API请求失败: {response.status_code}, {response.text}")
                return None, str(response.text)
        except Exception as e:
            logger.error(f"ai整理文档错误: {e}")
            return None, str(e)

    #  测试连接
    async def test_conn(self) -> Tuple[dict | None, str | None]:
        try:
            prompt = f"你是谁"
            headers = {
                "Content-Type": "application/json"
            }
            data = {
                "model": "llama3:8b",
                "messages": [
                    {
                        "role": "system",
                        "content": "你是一个ollama,最擅长的是帮助用户学习语言, 你现在22岁了"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    },
                
                ],
                "stream": False,
                "format": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string"
                        },
                        "age": {
                            "type": "integer"
                        },
                        "ability": {
                            "type": "string"
                        }
                    },
                    "required": ["name", "age", "ability"]
                },
                "options": {
                    "temperature": 0
                }
            }
            
            response = requests.post(
                os.environ.get("SELF_MODEL_API_URL"),
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"json: {result}")
                return result, None
            else:
                logger.error(f"API请求失败: {response.status_code}, {response.text}")
                return None, str(response.text)
        except Exception as e:
            logger.error(f"ai整理文档错误: {e}")
            return None, str(e)   

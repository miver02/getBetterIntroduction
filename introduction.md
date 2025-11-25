# 简历智能分析系统技术报告

## 一、项目概述

本项目是一个基于FastAPI框架开发的简历智能分析系统，能够接收用户上传的PDF格式简历文件，结合目标职位信息和筛选条件，通过调用Deepseek AI模型对简历进行解析、匹配度分析和排序，最终返回结构化的简历信息。系统主要应用于企业招聘场景，帮助HR快速筛选符合岗位要求的候选人。

## 二、系统架构

系统采用前后端分离架构，后端主要由以下核心模块组成：
- Web服务层：基于FastAPI构建，处理HTTP请求
- 文件处理层：负责上传文件的接收、存储和内容提取
- AI交互层：与Deepseek AI模型接口交互，实现简历分析
- 数据处理层：处理AI返回结果，提取结构化数据

架构流程图如下：
```
客户端 → FastFastAPI服务 → 
  ├─ 文件接收与存储模块
  ├─ PDF内容提取模块
  ├─ AI分析交互模块
  └─ 结果处理与返回模块
```

## 三、核心模块详解

### 3.1 Web服务模块（main.py）

该模块基于FastAPI构建，提供HTTP接口服务，主要包含：

1. **服务初始化**
```python
app = FastAPI()
```

2. **核心接口**
   - `POST /get_job/better_rank`：处理简历分析请求
   - `GET /`：返回前端页面

3. **文件处理流程**
   - 接收上传的PDF文件（支持单个文件和文件夹上传）
   - 创建并清理临时文件夹（`./pdf`）
   - 保存上传的文件到临时目录
   - 调用文件处理模块读取PDF内容
   - 调用AI分析模块处理简历信息
   - 返回处理结果

### 3.2 文件处理模块（HandleFiles类）

位于basecode.py中，负责PDF文件内容提取，主要功能：

1. **异步处理**：采用asyncio实现多文件并行处理，提高效率
```python
async def read_pdf(self, pdf_paths):
    tasks = []
    for pdf_path in pdf_paths:
        task = asyncio.create_task(self.get_fonts_with_pypdf(pdf_path))
        tasks.append(task)
    await asyncio.gather(*tasks)  
```

2. **PDF内容提取**：使用PyPDF2库提取PDF中的文本内容，按页面组织
```python
def get_fonts_with_pypdf(self, pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num, page in enumerate(pdf_reader.pages, 1):
            text = page.extract_text()
            if text.split():
                font_by_page[f"第{page_num}页"] = text
```

### 3.3 AI交互模块（ConnDeepseek类）

负责与Deepseek AI模型交互，实现简历分析和结构化处理：

1. **API配置**：通过环境变量获取API密钥，配置请求参数
```python
def __init__(self):
    self.api_key = os.environ.get('JINGLE_MINER_DEEPSEEK_V3')
```

2. **提示词设计**：构建精确的提示词，指导AI生成符合要求的JSON格式
```python
prompt = f"""我公司需要招聘{job}。读取{pdf_contents},理解文件内容和细节...
```

3. **JSON提取与处理**：实现多种JSON提取策略，处理可能的格式问题
```python
def extract_json_array(self, content):
    # 方法1: 从Markdown代码块中提取
    # 方法2: 直接查找有效的JSON数组
    # 方法3: 处理Extra data错误
    # 方法4: 修复常见JSON格式问题
```

## 四、API接口设计

### 4.1 简历分析接口

- **URL**: `/get_job/better_rank`
- **方法**: POST
- **请求参数**:
  - `job` (Form): 职位名称
  - `select` (Form): 筛选条件
  - `files` (File): 简历文件（可选）
  - `folder` (File): 文件夹中的简历文件（可选）

- **响应格式**:
```json
{
  "status": "success|false",
  "data": [
    {
      "name": "张三",
      "gender": "男",
      "age": 30,
      "work_years": 5,
      "work_experience": "...",
      "project_experience": "..."
    }
  ]
}
```

## 五、关键技术点

1. **异步处理**：结合FastAPI的异步特性和asyncio库，实现高效的文件并行处理
2. **健壮的JSON解析**：多种策略处理AI返回的JSON数据，提高系统容错性
3. **临时文件管理**：自动创建和清理临时文件目录，避免磁盘空间占用
4. **日志系统**：完善的日志记录，便于问题排查和系统监控

## 六、潜在优化方向

1. **文件类型验证**：增加更严格的文件类型和大小验证
2. **错误重试机制**：为AI接口调用增加重试机制，提高稳定性
3. **缓存机制**：对相同简历和职位的分析结果进行缓存，减少重复计算
4. **批量处理优化**：针对大量简历上传场景，实现分片处理
5. **安全性增强**：增加接口认证、文件上传安全验证等措施

## 七、总结

本系统通过结合FastAPI的高性能Web服务能力、PyPDF2的PDF处理能力和Deepseek AI的自然语言处理能力，实现了简历的自动化分析和筛选。系统架构清晰，模块职责明确，具有较好的可维护性和扩展性，能够有效提升企业招聘效率。
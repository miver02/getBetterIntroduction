# 智能简历筛选系统 (getBetterIntroduction)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991.svg?style=flat&logo=openai&logoColor=white)](https://openai.com/)

## 📝 项目介绍

智能简历筛选系统是一个基于 FastAPI 和大型语言模型的应用程序，旨在帮助企业和招聘团队自动化简历筛选流程。系统能够从 PDF 格式的简历中提取信息，并使用 AI 模型（DeepSeek V3）对简历进行智能分析和排序，帮助招聘人员快速找到最适合特定岗位的候选人。

### 核心功能

- 自动读取并解析 PDF 格式的简历文件
- 异步处理多份简历，提高处理效率
- 使用 DeepSeek V3 AI 模型分析简历内容
- 根据特定岗位需求对候选人进行智能排名
- 通过 RESTful API 接口提供服务

## 🛠️ 技术架构

- **后端框架**: FastAPI
- **API 服务器**: Uvicorn
- **PDF 处理**: PyPDF2
- **AI 模型**: DeepSeek V3 (通过 OpenRouter API)
- **异步处理**: asyncio

## 📋 项目结构

```
getBetterIntroduction/
├── main.py         # 主程序文件，包含 FastAPI 应用和主要逻辑
├── pdf/            # 存放待分析的简历 PDF 文件
│   ├── 简历1.pdf
│   ├── 简历2.pdf
│   └── 简历3.pdf
├── requirements.txt # 项目依赖
└── README.md        # 项目说明文档
```

## 🚀 安装指南

### 前置条件

- Python 3.8 或更高版本
- 有效的 DeepSeek API 密钥 (通过 OpenRouter)

### 安装步骤

1. 克隆项目仓库:

```bash
git clone https://github.com/yourusername/getBetterIntroduction.git
cd getBetterIntroduction
```

2. 安装所需依赖:

```bash
pip install -r requirements.txt
```

3. 设置环境变量:

```bash
# Linux/macOS
export My_DeepSeek_V3=your_api_key_here

# Windows
set DEEPSEEK_V3=your_api_key_here
```

## 📊 使用方法

### 准备工作

1. 将需要分析的简历 PDF 文件放入 `pdf` 文件夹中

### 启动服务

```bash
python main.py
```

服务将在 `http://0.0.0.0:8001` 上启动

### API 使用

#### 获取简历排名

```
GET /get_job/better_rank?job={岗位名称}
```

**参数**:
- `job`: 招聘岗位名称，例如"嵌入式应用开发工程师"

**返回**:
- 格式化的 JSON 数据，包含按岗位匹配度排序的简历信息

**示例请求**:
```bash
curl -X GET "http://localhost:8001/get_job/better_rank?job=嵌入式应用开发工程师"
```

## 🔄 工作流程

1. 系统启动时自动加载 `pdf` 文件夹中的所有简历
2. 使用 PyPDF2 异步提取所有简历的文本内容
3. 当收到 API 请求时，将简历内容和目标岗位信息发送给 DeepSeek AI 模型
4. AI 模型分析简历内容，提取关键信息并按岗位要求进行排序
5. 将排序后的结果以 JSON 格式返回给用户

## 📈 优化方向

- 添加简历预处理功能，提高文本提取质量
- 实现简历信息的结构化存储（例如数据库集成）
- 添加用户认证和权限控制
- 开发前端界面，提供更友好的用户体验
- 增加批量处理和导出功能

## 📄 许可证

[MIT License](LICENSE)

## 📧 联系方式

如有问题或建议，请联系：your-email@example.com
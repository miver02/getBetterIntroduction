# 构建阶段
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装项目依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 创建数据目录
RUN mkdir -p /app/pdf

# 复制项目文件
COPY . /app/

# 暴露端口
EXPOSE 8001

# 设置环境变量
ENV api_key = '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'

# 设置默认启动命令
CMD ["python", "main.py"]


# route_map.py
"""
API路由映射文件
================

此文件集中管理所有API路由路径，便于查阅和维护。
"""

# 测试路由
TEST_ROUTES = {
    "prefix": "/api/test",
    "tags": ["test"],
    "endpoints": {
        "test_conn_model": {
            "method": "POST",
            "path": "/test_conn_model",
            "summary": "测试模型连接",
            "description": "测试模型连接"
        },
    }
}

# 模型相关路由
MODELS_ROUTES = {
    "prefix": "/api/models",
    "tags": ["model"],
    "endpoints": {
        "create_model": {
            "method": "POST",
            "path": "/",
            "summary": "创建模型",
            "description": "创建新的模型"
        },
        "get_model": {
            "method": "GET",
            "path": "/{model_id}",
            "summary": "获取模型",
            "description": "获取指定模型"
        },
        "update_model": {
            "method": "PUT",
        },
        "get_rank": {
            "method": "POST",
            "path": "/get_rank",
            "summary": "获取获取排名",
            "description": "获取简历与职位契合度排名"
        },
    }
}

# 用户相关路由
USERS_ROUTES = {
    "prefix": "/api/users",
    "endpoints": {
        "create_user": {
            "method": "POST",
            "path": "/",
            "summary": "创建用户",
            "description": "创建新用户"
        },
        "get_user": {
            "method": "GET",
            "path": "/{user_id}",
            "summary": "获取用户",
            "description": "获取用户详情"
        }
    }
}

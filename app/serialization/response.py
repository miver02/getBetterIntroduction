# serialization/response.py
from pydantic import BaseModel
from typing import TypeVar, Generic, List, Optional, Any

T = TypeVar('T')

class BaseResponse(BaseModel):
    """基础响应模型"""
    code: int
    message: str
    data: Optional[Any] = None

class SuccessResponse(BaseResponse):
    """成功响应"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None

class ErrorResponse(BaseResponse):
    """错误响应"""
    code: int = 500
    message: str = "error"

# 使用泛型提高类型安全性
class ApiResponse(BaseModel, Generic[T]):
    """API 响应包装器"""
    status: str
    data: T
    message: str = "success"
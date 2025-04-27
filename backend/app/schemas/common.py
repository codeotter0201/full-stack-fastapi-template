import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from sqlmodel import SQLModel

# 定義通用類型變數
T = TypeVar("T")


class IDModel(SQLModel):
    """包含 ID 欄位的基礎模型"""

    id: uuid.UUID


class Message(SQLModel):
    """通用訊息模型"""

    message: str


class PaginationParams(SQLModel):
    """分頁參數模型"""

    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)


class PaginatedResponse(SQLModel, Generic[T]):
    """分頁回應模型"""

    data: list[T]
    count: int
    skip: int
    limit: int


class Token(SQLModel):
    """JWT 令牌模型"""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    """JWT 令牌內容模型"""

    sub: str | None = None


class NewPassword(SQLModel):
    """重置密碼模型"""

    token: str
    new_password: str = Field(min_length=8, max_length=40)

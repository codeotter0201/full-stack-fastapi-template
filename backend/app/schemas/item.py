import uuid

from pydantic import Field
from sqlmodel import SQLModel

from app.schemas.common import IDModel, PaginatedResponse


# 共用基礎物品屬性
class ItemBase(SQLModel):
    """物品基礎模型"""

    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# 物品建立請求
class ItemCreate(ItemBase):
    """物品建立請求模型"""

    pass


# 物品更新請求 - 所有欄位都是可選的
class ItemUpdate(SQLModel):
    """物品更新請求模型"""

    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# 物品公開回應
class ItemPublic(ItemBase, IDModel):
    """物品公開回應模型"""

    owner_id: uuid.UUID


# 物品詳細回應
class ItemDetail(ItemPublic):
    """物品詳細回應模型"""

    pass


# 物品列表回應
class ItemsPublic(PaginatedResponse[ItemPublic]):
    """物品列表回應模型"""

    pass

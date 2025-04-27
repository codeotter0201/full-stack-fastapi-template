from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from app.schemas.common import IDModel, PaginatedResponse


# 共用基礎用戶屬性
class UserBase(SQLModel):
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# 用戶建立請求
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


# 用戶註冊請求
class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# 用戶更新請求 - 所有欄位都是可選的
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = Field(default=None, max_length=255)


# 使用者自我更新請求 - 僅能更新部分欄位
class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


# 密碼更新請求
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# 用戶公開回應
class UserPublic(UserBase, IDModel):
    pass


# 用戶分頁回應
class UsersPublic(PaginatedResponse[UserPublic]):
    pass

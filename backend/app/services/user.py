import uuid
from typing import Optional, List

from sqlmodel import Session
from app.core.security import verify_password

from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserRegister
from app.tables import User


class UserService:
    """
    用戶服務層，處理用戶相關業務邏輯
    """

    def __init__(self, session: Session):
        self.session = session
        self.repository = UserRepository(session)

    def get(self, id: uuid.UUID) -> Optional[User]:
        """
        獲取單一用戶

        Args:
            id: 用戶 ID

        Returns:
            用戶對象
        """
        return self.repository.get_by_id(id)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        透過電子郵件取得用戶

        Args:
            email: 用戶電子郵件

        Returns:
            用戶對象
        """
        return self.repository.get_by_email(email)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        獲取所有用戶

        Args:
            skip: 跳過的數量
            limit: 限制的數量

        Returns:
            用戶列表
        """
        return self.repository.get_all(skip, limit)

    def create(self, user_create: UserCreate) -> User:
        """
        創建新用戶

        Args:
            user_create: 創建用戶的資料

        Returns:
            創建後的用戶
        """
        existing_user = self.repository.get_by_email(user_create.email)
        if existing_user:
            raise ValueError(f"電子郵件 {user_create.email} 已經被註冊")

        user_data = user_create.model_dump()
        return self.repository.create_with_password(user_data)

    def register(self, user_register: UserRegister) -> User:
        """
        用戶註冊

        Args:
            user_register: 用戶註冊資料

        Returns:
            創建後的用戶
        """
        existing_user = self.repository.get_by_email(user_register.email)
        if existing_user:
            raise ValueError(f"電子郵件 {user_register.email} 已經被註冊")

        user_data = user_register.model_dump()
        user_data.update({"is_active": True, "is_superuser": False})
        return self.repository.create_with_password(user_data)

    def update(self, id: uuid.UUID, user_update: UserUpdate) -> Optional[User]:
        """
        更新用戶資料

        Args:
            id: 用戶 ID
            user_update: 用戶更新資料

        Returns:
            更新後的用戶
        """
        user = self.repository.get_by_id(id)
        if not user:
            return None

        # 檢查電子郵件是否已存在
        if user_update.email and user_update.email != user.email:
            existing_user = self.repository.get_by_email(user_update.email)
            if existing_user:
                raise ValueError(f"電子郵件 {user_update.email} 已經被註冊")

        user_data = user_update.model_dump(exclude_unset=True)
        return self.repository.update_with_password(id, user_data)

    def delete(self, id: uuid.UUID) -> Optional[User]:
        """
        刪除用戶

        Args:
            id: 用戶 ID

        Returns:
            被刪除的用戶
        """
        return self.repository.delete(id)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        用戶認證

        Args:
            email: 電子郵件
            password: 密碼

        Returns:
            認證成功的用戶
        """
        return self.repository.authenticate(email, password)

    def update_password(
        self, user_id: uuid.UUID, current_password: str, new_password: str
    ) -> Optional[User]:
        """
        更新用戶密碼

        Args:
            user_id: 用戶 ID
            current_password: 當前密碼
            new_password: 新密碼

        Returns:
            更新後的用戶
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        # 驗證當前密碼
        if not verify_password(current_password, user.hashed_password):
            raise ValueError("當前密碼不正確")

        # 更新密碼
        return self.repository.update_with_password(user_id, {"password": new_password})

    def count(self) -> int:
        """
        計算用戶總數

        Returns:
            用戶總數
        """
        return self.repository.count()

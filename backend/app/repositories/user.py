import uuid
from typing import Optional

from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password

from app.repositories.base import BaseRepository
from app.models import User


class UserRepository(BaseRepository[User]):
    """
    用戶資料存取層，提供用戶資料的存取操作
    """

    def __init__(self, session: Session):
        """
        初始化用戶 Repository

        Args:
            session: 資料庫會話
        """
        super().__init__(session, User)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        透過電子郵件取得用戶

        Args:
            email: 用戶電子郵件

        Returns:
            找到的用戶，或 None
        """
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def create_with_password(self, obj_in: dict) -> User:
        """
        建立新用戶，包含密碼雜湊處理

        Args:
            obj_in: 用戶資料，包含明文密碼

        Returns:
            建立的用戶
        """
        password = obj_in.pop("password", None)
        if password:
            hashed_password = get_password_hash(password)
        else:
            hashed_password = ""

        db_obj = User(**obj_in, hashed_password=hashed_password)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update_with_password(self, id: uuid.UUID, obj_in: dict) -> Optional[User]:
        """
        更新用戶資料，包含密碼更新處理

        Args:
            id: 用戶 ID
            obj_in: 更新的用戶資料

        Returns:
            更新後的用戶
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        update_data = obj_in.copy()
        if "password" in update_data:
            hashed_password = get_password_hash(update_data.pop("password"))
            update_data["hashed_password"] = hashed_password

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def authenticate(self, email: str, password: str) -> Optional[User]:
        """
        驗證用戶資料

        Args:
            email: 用戶電子郵件
            password: 用戶密碼

        Returns:
            驗證成功的用戶，或 None
        """
        user = self.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        """
        檢查用戶是否啟用

        Args:
            user: 用戶

        Returns:
            是否啟用
        """
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        """
        檢查用戶是否為超級用戶

        Args:
            user: 用戶

        Returns:
            是否為超級用戶
        """
        return user.is_superuser

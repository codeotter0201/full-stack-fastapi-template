import uuid
from typing import Any, Generic, TypeVar, Type, List, Optional

from sqlmodel import Session, select, SQLModel

# 定義通用類型變數
T = TypeVar("T", bound=SQLModel)


class BaseRepository(Generic[T]):
    """
    所有 Repository 的基礎類別，提供通用的資料庫操作
    """

    def __init__(self, session: Session, model: Type[T]):
        """
        初始化 Repository

        Args:
            session: 資料庫會話
            model: SQLModel 模型類別
        """
        self.session = session
        self.model = model

    def get_by_id(self, id: uuid.UUID) -> Optional[T]:
        """
        透過 ID 取得單一項目

        Args:
            id: 項目 ID

        Returns:
            找到的項目，或 None
        """
        statement = select(self.model).where(self.model.id == id)
        return self.session.exec(statement).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """
        取得所有項目，支援分頁

        Args:
            skip: 跳過的項目數
            limit: 取得的項目數

        Returns:
            項目列表
        """
        statement = select(self.model).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def create(self, obj_in: Any) -> T:
        """
        建立新項目

        Args:
            obj_in: 輸入的物件資料

        Returns:
            建立的項目
        """
        db_obj = self.model.model_validate(obj_in)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def update(self, id: uuid.UUID, obj_in: Any) -> Optional[T]:
        """
        更新項目

        Args:
            id: 項目 ID
            obj_in: 更新的資料

        Returns:
            更新後的項目
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        update_data = obj_in
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        db_obj.sqlmodel_update(update_data)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def delete(self, id: uuid.UUID) -> Optional[T]:
        """
        刪除項目

        Args:
            id: 項目 ID

        Returns:
            被刪除的項目，或 None
        """
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        self.session.delete(db_obj)
        self.session.commit()
        return db_obj

    def count(self) -> int:
        """
        計算總項目數

        Returns:
            項目總數
        """
        statement = select(self.model)
        return len(self.session.exec(statement).all())

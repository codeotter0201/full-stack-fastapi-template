import uuid
from typing import List

from sqlmodel import Session, select

from app.repositories.base import BaseRepository
from app.tables import Item


class ItemRepository(BaseRepository[Item]):
    """
    物品資料存取層，提供物品資料的存取操作
    """

    def __init__(self, session: Session):
        """
        初始化物品 Repository

        Args:
            session: 資料庫會話
        """
        super().__init__(session, Item)

    def get_multi_by_owner(
        self, owner_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        取得特定用戶的所有物品

        Args:
            owner_id: 擁有者 ID
            skip: 跳過的項目數
            limit: 取得的項目數

        Returns:
            該用戶擁有的物品列表
        """
        statement = (
            select(Item).where(Item.owner_id == owner_id).offset(skip).limit(limit)
        )
        return self.session.exec(statement).all()

    def create_with_owner(self, obj_in: dict, owner_id: uuid.UUID) -> Item:
        """
        建立新物品，指定擁有者

        Args:
            obj_in: 物品資料
            owner_id: 擁有者 ID

        Returns:
            建立的物品
        """
        data = obj_in.copy()
        data["owner_id"] = owner_id

        db_obj = Item(**data)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def count_by_owner(self, owner_id: uuid.UUID) -> int:
        """
        計算特定用戶擁有的物品數量

        Args:
            owner_id: 擁有者 ID

        Returns:
            該用戶擁有的物品數量
        """
        statement = select(Item).where(Item.owner_id == owner_id)
        return len(self.session.exec(statement).all())

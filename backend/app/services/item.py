import uuid
from typing import List, Optional

from sqlmodel import Session

from app.repositories.item import ItemRepository
from app.repositories.user import UserRepository
from app.schemas.item import ItemCreate, ItemUpdate
from app.tables import Item, User


class ItemService:
    """
    物品服務層，處理物品相關業務邏輯
    """

    def __init__(self, session: Session):
        self.session = session
        self.repository = ItemRepository(session)
        self.user_repository = UserRepository(session)

    def get(self, id: uuid.UUID) -> Optional[Item]:
        """
        獲取單一物品

        Args:
            id: 物品 ID

        Returns:
            物品對象，如不存在則為 None
        """
        return self.repository.get_by_id(id)

    def get_multi(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """
        獲取多個物品

        Args:
            skip: 跳過的項目數
            limit: 取得的項目數

        Returns:
            物品列表
        """
        return self.repository.get_all(skip=skip, limit=limit)

    def get_multi_by_owner(
        self, owner_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        """
        獲取特定用戶的所有物品

        Args:
            owner_id: 擁有者 ID
            skip: 跳過的項目數
            limit: 取得的項目數

        Returns:
            該用戶的物品列表
        """
        return self.repository.get_multi_by_owner(
            owner_id=owner_id, skip=skip, limit=limit
        )

    def create(self, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
        """
        創建新物品

        Args:
            item_in: 物品建立資料
            owner_id: 擁有者 ID

        Returns:
            建立的物品
        """
        # 檢查用戶是否存在
        user = self.user_repository.get_by_id(owner_id)
        if not user:
            raise ValueError(f"用戶 ID {owner_id} 不存在")

        item_data = item_in.model_dump()
        return self.repository.create_with_owner(obj_in=item_data, owner_id=owner_id)

    def update(
        self, id: uuid.UUID, item_in: ItemUpdate, current_user: User
    ) -> Optional[Item]:
        """
        更新物品資料

        Args:
            id: 物品 ID
            item_in: 更新的物品資料
            current_user: 當前用戶

        Returns:
            更新後的物品

        Raises:
            ValueError: 如果物品不存在或當前用戶無權限更新
        """
        item = self.repository.get_by_id(id)
        if not item:
            raise ValueError(f"物品 ID {id} 不存在")

        # 檢查權限，只有物品擁有者或超級用戶可以更新
        if not current_user.is_superuser and item.owner_id != current_user.id:
            raise ValueError("沒有權限更新此物品")

        item_data = item_in.model_dump(exclude_unset=True)
        return self.repository.update(id=id, obj_in=item_data)

    def delete(self, id: uuid.UUID, current_user: User) -> Optional[Item]:
        """
        刪除物品

        Args:
            id: 物品 ID
            current_user: 當前用戶

        Returns:
            刪除的物品

        Raises:
            ValueError: 如果物品不存在或當前用戶無權限刪除
        """
        item = self.repository.get_by_id(id)
        if not item:
            raise ValueError(f"物品 ID {id} 不存在")

        # 檢查權限，只有物品擁有者或超級用戶可以刪除
        if not current_user.is_superuser and item.owner_id != current_user.id:
            raise ValueError("沒有權限刪除此物品")

        return self.repository.delete(id=id)

    def count(self) -> int:
        """
        計算物品總數

        Returns:
            物品總數
        """
        return self.repository.count()

    def count_by_owner(self, owner_id: uuid.UUID) -> int:
        """
        計算特定用戶擁有的物品數量

        Args:
            owner_id: 擁有者 ID

        Returns:
            該用戶擁有的物品數量
        """
        return self.repository.count_by_owner(owner_id)

"""
測試 ItemService 功能
"""

from sqlmodel import Session

from app.services.item import ItemService
from app.services.user import UserService
from app.schemas import ItemCreate, ItemUpdate, UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_item(db: Session) -> None:
    """測試創建項目"""
    # 先創建用戶
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)

    # 創建項目
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item_service = ItemService(db)

    if user.id:
        item = item_service.create(item_in=item_in, owner_id=user.id)
        assert item.title == title
        assert item.description == description
        assert item.owner_id == user.id


def test_get_item(db: Session) -> None:
    """測試獲取項目"""
    # 先創建用戶
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)

    # 創建項目
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item_service = ItemService(db)

    if user.id:
        item = item_service.create(item_in=item_in, owner_id=user.id)
        item_id = item.id

        # 獲取項目
        if item_id:
            db_item = item_service.get(item_id)
            assert db_item
            assert db_item.title == title
            assert db_item.description == description
            assert db_item.owner_id == user.id


def test_update_item(db: Session) -> None:
    """測試更新項目"""
    # 先創建用戶
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)

    # 創建項目
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item_service = ItemService(db)

    if user.id:
        item = item_service.create(item_in=item_in, owner_id=user.id)
        item_id = item.id

        # 更新項目
        if item_id:
            new_title = random_lower_string()
            new_description = random_lower_string()
            item_update = ItemUpdate(title=new_title, description=new_description)

            updated_item = item_service.update(
                id=item_id, item_in=item_update, current_user=user
            )
            assert updated_item
            assert updated_item.title == new_title
            assert updated_item.description == new_description
            assert updated_item.owner_id == user.id


def test_delete_item(db: Session) -> None:
    """測試刪除項目"""
    # 先創建用戶
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)

    # 創建項目
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item_service = ItemService(db)

    if user.id:
        item = item_service.create(item_in=item_in, owner_id=user.id)
        item_id = item.id

        # 刪除項目
        if item_id:
            deleted_item = item_service.delete(id=item_id, current_user=user)
            assert deleted_item

            # 確認項目已被刪除
            db_item = item_service.get(item_id)
            assert db_item is None


def test_get_multi(db: Session) -> None:
    """測試獲取多個項目"""
    # 先創建用戶
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)

    if not user.id:
        return

    # 創建多個項目
    item_service = ItemService(db)
    items_count = 5
    for _ in range(items_count):
        title = random_lower_string()
        description = random_lower_string()
        item_in = ItemCreate(title=title, description=description)
        item_service.create(item_in=item_in, owner_id=user.id)

    # 獲取項目並檢查數量
    items = item_service.get_multi_by_owner(owner_id=user.id, skip=0, limit=10)
    assert len(items) >= items_count  # 可能有其他測試的項目

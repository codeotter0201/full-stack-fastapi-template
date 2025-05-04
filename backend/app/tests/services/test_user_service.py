"""
測試 UserService 功能
"""

from fastapi.encoders import jsonable_encoder
from sqlmodel import Session

from app.services.user import UserService
from app.core.security import verify_password
from app.models import User
from app.schemas import UserCreate, UserUpdate, UserRegister
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    """測試創建用戶"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_register_user(db: Session) -> None:
    """測試註冊用戶"""
    email = random_email()
    password = random_lower_string()
    user_in = UserRegister(email=email, password=password)
    user_service = UserService(db)
    user = user_service.register(user_in)
    assert user.email == email
    assert user.is_active is True
    assert user.is_superuser is False
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    """測試用戶認證"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)
    authenticated_user = user_service.authenticate(email, password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    """測試用戶認證失敗"""
    email = random_email()
    password = random_lower_string()
    user_service = UserService(db)
    user = user_service.authenticate(email, password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    """測試檢查用戶是否活躍"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)
    assert user.is_active is True


def test_check_if_user_is_active_inactive(db: Session) -> None:
    """測試檢查停用用戶是否活躍"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, disabled=True)
    user_service = UserService(db)
    user = user_service.create(user_in)
    assert user.is_active


def test_check_if_user_is_superuser(db: Session) -> None:
    """測試檢查用戶是否為超級用戶"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user_service = UserService(db)
    user = user_service.create(user_in)
    assert user.is_superuser is True


def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
    """測試檢查普通用戶是否為超級用戶"""
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)
    assert user.is_superuser is False


def test_get_user(db: Session) -> None:
    """測試獲取用戶"""
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user_service = UserService(db)
    user = user_service.create(user_in)
    user_2 = db.get(User, user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_get_user_by_email(db: Session) -> None:
    """測試透過電子郵件獲取用戶"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)
    db_user = user_service.get_by_email(email)
    assert db_user
    assert user.email == db_user.email
    assert jsonable_encoder(user) == jsonable_encoder(db_user)


def test_update_user(db: Session) -> None:
    """測試更新用戶"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)

    new_password = random_lower_string()
    new_email = random_email()
    user_update = UserUpdate(email=new_email, password=new_password)

    if user.id:
        updated_user = user_service.update(user.id, user_update)
        assert updated_user
        assert updated_user.email == new_email
        assert verify_password(new_password, updated_user.hashed_password)


def test_delete_user(db: Session) -> None:
    """測試刪除用戶"""
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user_service = UserService(db)
    user = user_service.create(user_in)

    if user.id:
        user_service.delete(user.id)
        deleted_user = user_service.get(user.id)
        assert deleted_user is None


def test_count_users(db: Session) -> None:
    """測試計算用戶數量"""
    initial_count = UserService(db).count()

    # 創建幾個測試用戶
    for _ in range(3):
        email = random_email()
        password = random_lower_string()
        user_in = UserCreate(email=email, password=password)
        user_service = UserService(db)
        user_service.create(user_in)

    final_count = UserService(db).count()
    assert final_count == initial_count + 3

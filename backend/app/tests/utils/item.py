from sqlmodel import Session

from app.services.item import ItemService
from app.models import Item
from app.schemas import ItemCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_item(db: Session) -> Item:
    user = create_random_user(db)
    owner_id = user.id
    assert owner_id is not None
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    item_service = ItemService(db)
    return item_service.create(item_in=item_in, owner_id=owner_id)

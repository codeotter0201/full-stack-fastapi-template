from fastapi.testclient import TestClient
from collections.abc import Generator
from sqlmodel import Session, delete

# from pytest_mock import MockerFixture
import pytest
import docker
import time

import app.tests.overide_settings
from app.core.config import settings
from app.core.db import init_db, engine
from app.main import app
from app.models import Item, User
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def postgres_container():
    client = docker.from_env()
    container = client.containers.run(
        "postgres:15",
        environment={
            "POSTGRES_USER": settings.POSTGRES_USER,
            "POSTGRES_PASSWORD": settings.POSTGRES_PASSWORD,
            "POSTGRES_DB": settings.POSTGRES_DB,
        },
        ports={"5432/tcp": settings.POSTGRES_PORT},
        detach=True,
    )
    time.sleep(5)  # 等待 PostgreSQL 啟動
    yield
    container.stop()
    container.remove()


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        # 清理測試資料
        statement = delete(Item)
        session.exec(statement)
        statement = delete(User)
        session.exec(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )

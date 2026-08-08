import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config.settings import Settings
from app.database.base import Base
from app.database.database import get_db
from app.main import app

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", Settings().database_url)


def _database_is_reachable(engine: Engine) -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return False
    return True


def _prepare_schema(engine: Engine) -> None:
    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def test_database() -> Generator:
    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    if not _database_is_reachable(engine):
        engine.dispose()
        pytest.skip("test database is not reachable")
    _prepare_schema(engine)
    yield engine
    engine.dispose()


@pytest.fixture()
def db_session(test_database: Engine) -> Generator[Session, None, None]:
    connection = test_database.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        transaction.rollback()
        session.close()
        connection.close()


@pytest.fixture(autouse=True)
def _mock_repository() -> Generator[None, None, None]:
    yield


@pytest.fixture(autouse=True)
def _override_get_db(db_session: Session) -> Generator[None, None, None]:
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
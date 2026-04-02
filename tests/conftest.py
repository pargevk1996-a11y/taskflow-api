import os
import sys
from collections.abc import Generator
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("JWT_SECRET_KEY", "test_secret_key")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///./test_taskflow.db")

from app.db.base import Base  # noqa: E402
from app.api.deps import get_db as app_get_db  # noqa: E402
from app.main import app as fastapi_app  # noqa: E402
import app.models  # noqa: F401,E402


engine = create_engine("sqlite+pysqlite:///./test_taskflow.db", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


def override_get_db() -> Generator[Session, None, None]:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def db() -> Generator[Session, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest_asyncio.fixture()
async def api_client() -> Generator[AsyncClient, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    fastapi_app.dependency_overrides[app_get_db] = override_get_db

    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

    fastapi_app.dependency_overrides.clear()

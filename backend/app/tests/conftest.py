import os
import sys

import pytest
from asgi_lifespan import LifespanManager
from sqlalchemy import text

# Добавляем папку backend в sys.path
backend_path = os.path.dirname(os.path.dirname(__file__))
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Импортируем из пакета app
from db.session import async_session_factory, engine
from models import Base
from main import app

from httpx import AsyncClient, ASGITransport


@pytest.fixture
async def async_client():
    """Асинхронный тест-клиент FastAPI с корректным запуском startup/shutdown."""
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            yield client


@pytest.fixture(scope="session", autouse=True)
async def create_tables():
    """Создает таблицы перед тестами и удаляет после всех тестов."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
async def setup_db():
    """Очищает таблицу user перед каждым тестом."""
    async with async_session_factory() as session:
        await session.execute(text("DELETE FROM user"))
        await session.commit()

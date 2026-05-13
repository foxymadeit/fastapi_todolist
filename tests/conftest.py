import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app
from database import ASYNC_DATABASE_URL, get_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client():
    engine = create_async_engine(ASYNC_DATABASE_URL)
    TestSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def override_get_session():
        async with TestSession() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()




@pytest_asyncio.fixture(scope="session")
async def test_token(client):
    login = await client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "testpassword"
    })
    if login.status_code != 200:
        await client.post("/auth/register", json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword"
        })
        login = await client.post("/auth/login", json={
            "email": "test@test.com",
            "password": "testpassword"
        })
    return login.json()["access_token"]


@pytest_asyncio.fixture(scope="session")
async def test_task(client, test_token):
    response = await client.post("/tasks",
        json={"task_title": "test task"},
        headers={"Authorization": f"Bearer {test_token}"}
    )
    return response.json()

@pytest_asyncio.fixture(scope="session")
async def test_updated_task(client, test_token):
    task = {"task_title": "test task",
            "is_completed": True}
    
    return task
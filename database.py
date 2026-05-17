from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import settings



USER = settings.POSTGRES_USER
PASSWORD = settings.POSTGRES_PASSWORD.get_secret_value()
HOST = settings.POSTGRES_HOST
PORT = settings.POSTGRES_PORT
DB_NAME = settings.POSTGRES_DB

ASYNC_DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
SYNC_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_async_engine(ASYNC_DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)
print(f"DATABASE_URL: {ASYNC_DATABASE_URL}")

# Base Class for table creation
class Base(DeclarativeBase):
    pass


# Session creation
async def get_session():
    async with new_session() as session:
        yield session


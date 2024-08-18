from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def create_db_and_tables():
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    print("Tables created!")


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

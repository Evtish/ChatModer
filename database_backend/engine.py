from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine

from system.settings import DB_NAME
from . import Base

db_engine = create_async_engine(
    f'sqlite+aiosqlite:///{DB_NAME}',
    echo=False
)

session_factory = async_sessionmaker(db_engine)


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def sqlalchemy_main() -> None:
    await create_tables(db_engine)

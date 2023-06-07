from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta
from config import settings


# 'postgresql://<username>:<password>@<ip-adress/hostname>:portnumber/<database_name>'
DATABASE_URL = f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}"


engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)


async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False,
)


async def get_session():
    async with async_session() as session:
        assert isinstance(session, AsyncSession)
        yield session


Base: DeclarativeMeta = declarative_base()


async def connect() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        print("datapase is connected successfully...")


async def disconnect() -> None:
    if engine:
        await engine.dispose()
        print("datapase is disconnected successfully...")

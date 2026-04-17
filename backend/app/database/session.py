# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session

from app.config import db_settings

engine = create_async_engine(
    # url = "sqlite:///sqlite.db",
    url=db_settings.POSTGRES_URL,
    echo=True,
    # connect_args={"check_same_thread": False}
)


async def create_db_and_tables():
    async with engine.begin() as connection:
        from app.database.models import Shipment, Seller

        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from config.settings import settings

async_engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionFactory = async_sessionmaker(bind=async_engine, expire_on_commit=False)


async def get_async_db():
    async_session = AsyncSessionFactory()
    try:
        yield async_session
    finally:
        await async_session.close()


class Base(DeclarativeBase):
    pass


class CommonMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

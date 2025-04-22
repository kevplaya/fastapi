from datetime import datetime

from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, sessionmaker

from config.settings import settings

engine = create_engine(settings.database_url)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


class Base(DeclarativeBase):
    pass


class CommonMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

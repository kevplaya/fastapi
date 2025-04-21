from datetime import datetime

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base
from models.company import CompanyTag


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    name: Mapped[list["TagName"]] = relationship(
        back_populates="tag", cascade="all, delete"
    )
    company: Mapped[list["CompanyTag"]] = relationship(
        back_populates="tag", cascade="all, delete"
    )


class TagName(Base):
    __tablename__ = "tag_name"
    __table_args__ = (Index("ix_tag_name_lang_name", "lang", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), nullable=False
    )
    lang: Mapped[str] = mapped_column(String(5), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    tag: Mapped["Tag"] = relationship(back_populates="name")

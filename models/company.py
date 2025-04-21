from datetime import datetime

from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base
from models.tag import Tag


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )

    name: Mapped[list["CompanyName"]] = relationship(
        back_populates="company", cascade="all, delete"
    )
    tag: Mapped[list["CompanyTag"]] = relationship(
        back_populates="company", cascade="all, delete"
    )


class CompanyName(Base):
    __tablename__ = "company_name"
    __table_args__ = (Index("ix_company_name_lang_name", "lang", "name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    lang: Mapped[str] = mapped_column(String(5), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    company: Mapped["Company"] = relationship(back_populates="name")


class CompanyTag(Base):
    __tablename__ = "company_tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), index=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), index=True
    )

    company: Mapped["Company"] = relationship(back_populates="tag")
    tag: Mapped["Tag"] = relationship(back_populates="company")

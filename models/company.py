from pydantic import BaseModel
from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base, CommonMixin


class CompanySearchResponse(BaseModel):
    company_name: str


class Company(Base, CommonMixin):
    name: Mapped[list["CompanyName"]] = relationship(back_populates="company", cascade="all, delete")
    tag: Mapped[list["CompanyTag"]] = relationship(back_populates="company", cascade="all, delete")

    names: Mapped[list["CompanyName"]] = relationship(
        "CompanyName", back_populates="company", lazy="selectin", overlaps="name"
    )
    tags: Mapped[list["Tag"]] = relationship(  # noqa: F821
        "Tag",
        secondary="companytag",
        back_populates="companies",
        lazy="selectin",
        overlaps="company,tag",
    )


class CompanyName(Base, CommonMixin):
    __table_args__ = (
        Index("ix_company_name_lang_name", "lang", "name"),
        UniqueConstraint("company_id", "lang", "name", name="uq_company_lang_name_pair"),
    )

    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), nullable=False)
    lang: Mapped[str] = mapped_column(String(5), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    company: Mapped["Company"] = relationship(back_populates="name")


class CompanyTag(Base, CommonMixin):
    __table_args__ = (UniqueConstraint("company_id", "tag_id", name="uq_company_tag_pair"),)
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id", ondelete="CASCADE"), index=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id", ondelete="CASCADE"), index=True)

    company: Mapped["Company"] = relationship(back_populates="tag")
    tag: Mapped["Tag"] = relationship(back_populates="company")  # noqa: F821

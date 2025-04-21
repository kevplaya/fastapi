from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base, CommonMixin


class Company(Base, CommonMixin):
    name: Mapped[list["CompanyName"]] = relationship(
        back_populates="company", cascade="all, delete"
    )
    tag: Mapped[list["CompanyTag"]] = relationship(
        back_populates="company", cascade="all, delete"
    )


class CompanyName(Base, CommonMixin):
    __table_args__ = (Index("ix_company_name_lang_name", "lang", "name"),)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), nullable=False
    )
    lang: Mapped[str] = mapped_column(String(5), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    company: Mapped["Company"] = relationship(back_populates="name")


class CompanyTag(Base, CommonMixin):
    company_id: Mapped[int] = mapped_column(
        ForeignKey("company.id", ondelete="CASCADE"), index=True
    )
    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), index=True
    )

    company: Mapped["Company"] = relationship(back_populates="tag")
    tag: Mapped["Tag"] = relationship(back_populates="company")  # noqa: F821

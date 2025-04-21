from sqlalchemy import ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base, CommonMixin


class Tag(Base, CommonMixin):
    name: Mapped[list["TagName"]] = relationship(
        back_populates="tag", cascade="all, delete"
    )
    company: Mapped[list["CompanyTag"]] = relationship(  # noqa: F821
        back_populates="tag", cascade="all, delete"
    )


class TagName(Base, CommonMixin):
    __table_args__ = (Index("ix_tag_name_lang_name", "lang", "name"),)

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tag.id", ondelete="CASCADE"), nullable=False
    )
    lang: Mapped[str] = mapped_column(String(5), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    tag: Mapped["Tag"] = relationship(back_populates="name")

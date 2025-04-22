from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base, CommonMixin


class Tag(Base, CommonMixin):
    name: Mapped[list["TagName"]] = relationship(back_populates="tag", cascade="all, delete")
    company: Mapped[list["CompanyTag"]] = relationship(back_populates="tag", cascade="all, delete")  # noqa: F821

    names: Mapped[list["TagName"]] = relationship("TagName", back_populates="tag", lazy="selectin", overlaps="name")
    companies: Mapped[list["Company"]] = relationship(  # noqa: F821
        "Company", secondary="companytag", back_populates="tags", lazy="selectin", overlaps="company,tag"
    )


class TagName(Base, CommonMixin):
    __table_args__ = (
        Index("ix_tag_name_lang_name", "lang", "name"),
        UniqueConstraint("tag_id", "lang", "name", name="uq_tag_lang_name"),
    )

    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id", ondelete="CASCADE"), nullable=False)
    lang: Mapped[str] = mapped_column(String(5), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    tag: Mapped["Tag"] = relationship(back_populates="name")

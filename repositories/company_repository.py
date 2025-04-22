from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.company import Company, CompanyName
from models.tag import Tag


class CompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def autocomplete_company_name(self, keyword: str, lang: str) -> list[str]:
        stmt = (
            select(CompanyName.name)
            .join(Company)
            .where(CompanyName.lang == lang)
            .where(CompanyName.name.like(f"%{keyword}%"))
            .order_by(desc(CompanyName.name))
        )
        result = self.session.execute(stmt)
        return [row[0] for row in result.fetchall()]

    def search_company_by_name(self, keyword: str) -> list[Company]:
        stmt = (
            select(Company)
            .options(selectinload(Company.names), selectinload(Company.tags).selectinload(Tag.names))
            .join(CompanyName)
            .where(CompanyName.name == keyword)
        )
        result = self.session.execute(stmt)
        return result.scalars().first()

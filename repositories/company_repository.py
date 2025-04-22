from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.company import Company, CompanyName


class CompanyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def autocomplete_company_name(self, keyword: str, lang: str) -> list[str]:
        stmt = (
            select(CompanyName.name)
            .join(Company)
            .where(CompanyName.lang == lang)
            .where(CompanyName.name.like(f"%{keyword}%"))
            .order_by(desc(CompanyName.name))
        )
        result = await self.session.execute(stmt)
        return [row[0] for row in result.fetchall()]

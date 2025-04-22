from repositories.company_repository import CompanyRepository


class CompanyService:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    async def get_autocomplete_company_names(self, keyword: str, lang: str):
        names = await self.company_repository.autocomplete_company_name(keyword, lang)
        return [{"company_name": name} for name in names]

    async def search_companies_by_name(self, keyword: str, lang: str):
        company = await self.company_repository.search_company_by_name(keyword)
        if not company:
            return []

        return {
            "company_name": next((name.name for name in company.names if name.lang == lang), ""),
            "tags": [tag_name.name for tag in company.tags for tag_name in tag.names if tag_name.lang == lang],
        }

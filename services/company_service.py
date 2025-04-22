from repositories.company_repository import CompanyRepository


class CompanyService:
    def __init__(self, company_repository: CompanyRepository):
        self.company_repository = company_repository

    async def get_autocomplete_company_names(self, keyword: str, lang: str):
        names = await self.company_repository.autocomplete_company_name(keyword, lang)
        return [{"company_name": name} for name in names]

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_async_db
from routers.company import CompanyRouter

app = FastAPI()
app.include_router(
    CompanyRouter,
)


@app.get("/ping")
async def ping(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(text("SELECT 1"))
    scalar_value = result.scalar()
    return {"message": bool(scalar_value)}

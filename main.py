from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from config.database import get_db
from routers.company import CompanyRouter

app = FastAPI()
app.include_router(
    CompanyRouter,
)


@app.get("/ping")
def ping(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    scalar_value = result.scalar()
    return {"message": bool(scalar_value)}

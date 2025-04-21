from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from config.database import get_db

app = FastAPI()


@app.get("/ping")
def ping(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1")).scalar()
    return {"message": bool(result)}

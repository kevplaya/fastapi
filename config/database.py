from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.settings import settings

DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

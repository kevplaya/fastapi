import csv
import time

from consts import (
    COMPANY_NAME_PREFIX,
    COMPANY_TAG_PREFIX,
    INPUT_COMPANY_TAG_CSV_FILE,
    LANGS,
    OUTPUT_TAG_CSV_FILE,
    TAG_DELIMITER,
)
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings
from models.company import Company, CompanyName, CompanyTag
from models.tag import Tag, TagName

engine = create_engine(settings.database_url.replace("aiomyql", "pymysql"))
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


def find_existing_tag_by_names(session: Session, names: dict) -> Tag | None:
    for lang, name in names.items():
        result = session.execute(select(Tag).join(TagName).where(TagName.lang == lang, TagName.name == name))
        tag = result.scalar_one_or_none()
        if tag:
            return tag
    return None


def insert_tags_from_csv(session: Session):
    with open(OUTPUT_TAG_CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tag_names = {lang: row.get(f"tag_{lang}", "").strip() for lang in LANGS if row.get(f"tag_{lang}")}
            if not tag_names:
                continue

            existing_tag = find_existing_tag_by_names(session, tag_names)
            if existing_tag:
                continue

            tag = Tag()
            session.add(tag)
            session.flush()

            for lang, name in tag_names.items():
                session.add(TagName(tag_id=tag.id, lang=lang, name=name))


def insert_companies_and_tags(session: Session):
    with open(INPUT_COMPANY_TAG_CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            company = Company()
            session.add(company)
            session.flush()

            for lang in LANGS:
                name = row.get(f"{COMPANY_NAME_PREFIX}{lang}", "").strip()
                if name:
                    session.add(CompanyName(company_id=company.id, lang=lang, name=name))

            tags_by_lang = {
                lang: [t.strip() for t in row.get(f"{COMPANY_TAG_PREFIX}{lang}", "").split(TAG_DELIMITER)]
                for lang in LANGS
            }
            max_len = max(len(tags_by_lang[lang]) for lang in LANGS)

            for i in range(max_len):
                tag_names = {
                    lang: tags_by_lang[lang][i]
                    for lang in LANGS
                    if i < len(tags_by_lang[lang]) and tags_by_lang[lang][i]
                }

                if not tag_names:
                    continue

                tag = find_existing_tag_by_names(session, tag_names)
                if tag:
                    session.add(CompanyTag(company_id=company.id, tag_id=tag.id))


def load_data():
    start = time.perf_counter()
    with SessionFactory() as session:
        insert_tags_from_csv(session)
        insert_companies_and_tags(session)
        session.commit()
    end = time.perf_counter()
    print(f"time: {end - start:.2f}초")


if __name__ == "__main__":
    load_data()

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")


# Echo는 SQL문을 출력해준다.(디버깅용)
engin = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(autoflush=False, autocommit=False, bind=engin)


# generator를 사용해서 session을 생성한다.
def get_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

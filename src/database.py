from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from starlette.requests import Request

DATABASE_URL = "sqlite:///./sistemaescolar.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db(request: Request):
    db = SessionLocal()
    try:
        yield db
        db.commit()  # garante commit no final da requisição
    except Exception:
        db.rollback()  # se deu erro, volta
        raise
    finally:
        db.close()

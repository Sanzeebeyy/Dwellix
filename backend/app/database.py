from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DB_URL = "postgresql+psycopg2://postgres:Sanjeeb5622@localhost:5432/Dwellix"

engine = create_engine(SQLALCHEMY_DB_URL)
LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit= False)
Base = declarative_base()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


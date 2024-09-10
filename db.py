from sqlalchemy import create_engine, MetaData, URL
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)
SessionDB = sessionmaker(engine, autocommit=False, autoflush=True)  
metadata = MetaData()
def get_db():
    db = SessionDB()
    try:
        yield db
    finally:
        db.close()
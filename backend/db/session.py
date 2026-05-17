import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Build an absolute path to the database file in the backend folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'gousto-v3.db')}"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

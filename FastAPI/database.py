from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

URL_DATABASE = "sqlite:///./plants.db"

engine = create_engine(URL_DATABASE, connect_args={"check_same_thread": False})

# SessionLocal = sessionmaker(autocomit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

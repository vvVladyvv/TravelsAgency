from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

engine = create_engine(
    url=settings.DATABASE_URL
)

sessionlocal = sessionmaker(
    bind=engine,
    autoflush=False,
)

def get_db():
    session = sessionlocal()
    try:
        yield session
    finally:
        session.close()

Base = declarative_base()


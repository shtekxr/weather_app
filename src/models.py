from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base


DATABASE_URL = "sqlite:///../test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CityHistory(Base):
    __tablename__ = "city_history"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    count = Column(Integer, default=0)

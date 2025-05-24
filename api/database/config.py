from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from decouple import config


class Base(DeclarativeBase):
    pass


DATABASE_URL: str = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(engine)

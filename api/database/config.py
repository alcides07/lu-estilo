from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from decouple import config


class Base(DeclarativeBase):
    pass


DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///database.db")

connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
Session = sessionmaker(engine)

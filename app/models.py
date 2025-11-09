from sqlalchemy import Column, Integer, Date, Text, Numeric
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, primary_key=True, index=True)
    name = Column(Text)


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, index=True)
    release_date = Column(Date, nullable=True)
    rating = Column(Numeric(2, 1), nullable=True)

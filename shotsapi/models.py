from enum import unique
from sqlalchemy import Boolean, Column, Integer, SmallInteger, String
from sqlalchemy.orm import relationship

from .database import Base


class Blob(Base):
    __tablename__ = "blobs"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String)
    order = Column(SmallInteger, index=True)
    type = Column(String, index=True)

    owner = relationship("Shots", back_populates="images")


class Shots(Base):
    __tablename__ = "blobs"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    images = relationship("Blob", back_populates="owner")

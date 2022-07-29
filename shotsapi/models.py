from sqlalchemy import Column, Integer, SmallInteger, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Blob(Base):
    __tablename__ = "blobs"

    id = Column(Integer, primary_key=True)
    shots_id = Column(Integer, ForeignKey("shots.id"))
    name = Column(String, unique=True)
    url = Column(String)
    order = Column(SmallInteger, index=True)
    type = Column(String, index=True)

    owner = relationship("Shots", back_populates="images")


class Shots(Base):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    images = relationship("Blob", back_populates="owner")

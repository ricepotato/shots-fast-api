from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    String,
    ForeignKey,
    Table,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

association_table = Table(
    "shot_tag",
    Base.metadata,
    Column("shots_id", ForeignKey("shots.id")),
    Column("tags_id", ForeignKey("blobs.id")),
)


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


class Blob(Base):
    __tablename__ = "blobs"

    id = Column(Integer, primary_key=True)
    shots_id = Column(Integer, ForeignKey("shots.id"))
    name = Column(String(50), unique=True)
    url = Column(String(1000))
    order = Column(SmallInteger, index=True)
    type = Column(String(20), index=True)
    time_created = Column(DateTime, server_default=func.now())
    time_updated = Column(DateTime, onupdate=func.now())

    owner = relationship("Shots", back_populates="images")


class Shots(Base):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    custom = Column(String, index=True)
    status = Column(String, default=None)
    time_created = Column(DateTime, server_default=func.now())
    time_updated = Column(DateTime, onupdate=func.now())

    images = relationship("Blob", back_populates="owner")

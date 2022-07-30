from sqlalchemy import Column, Integer, SmallInteger, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    name = Column(String, unique=True)


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
    custom = Column(String, index=True)

    images = relationship("Blob", back_populates="owner")

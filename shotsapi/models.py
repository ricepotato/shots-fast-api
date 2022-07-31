from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    String,
    ForeignKey,
    Table,
    DateTime,
)
from sqlalchemy.orm import relationship, declarative_base, declared_attr
from sqlalchemy.sql import func

Base = declarative_base()

association_table = Table(
    "shot_tag",
    Base.metadata,
    Column("shots_id", ForeignKey("shots.id")),
    Column("tags_id", ForeignKey("blobs.id")),
)


class TimestamedTable:
    @declared_attr
    def time_created(self):
        return Column(DateTime, server_default=func.now())

    @declared_attr
    def time_updated(self):
        return Column(DateTime, onupdate=func.now())


class Tags(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


class Blob(Base, TimestamedTable):
    __tablename__ = "blobs"

    id = Column(Integer, primary_key=True)
    shots_id = Column(Integer, ForeignKey("shots.id"))
    name = Column(String(100), unique=True)
    url = Column(String(1000))
    order = Column(SmallInteger, index=True)
    type = Column(String(20), index=True)

    owner = relationship("Shots", back_populates="images")


class Shots(Base, TimestamedTable):
    __tablename__ = "shots"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    custom = Column(String(50), index=True, default=None)
    status = Column(String(20), default=None)
    description = Column(String(100), default=None)

    images = relationship("Blob", back_populates="owner")

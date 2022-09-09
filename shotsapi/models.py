from email.policy import default
from typing import List
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
from sqlalchemy.sql import func, asc

Base = declarative_base()

shot_tag_table = Table(
    "shot_tag",
    Base.metadata,
    Column("shots_id", ForeignKey("shot.id")),
    Column("tags_id", ForeignKey("tag.id")),
)


# shot_blob_table = Table(
#     "shot_blob",
#     Base.metadata,
#     Column("shots_id", ForeignKey("shot.id")),
#     Column("blob_id", ForeignKey("blob.id")),
# )


class TimestamedTable:
    @declared_attr
    def time_created(self):
        return Column(DateTime, server_default=func.now())

    @declared_attr
    def time_updated(self):
        return Column(DateTime, onupdate=func.now())


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)


class ShotBlob(Base):
    __tablename__ = "shot_blob"

    shots_id = Column(ForeignKey("shot.id"), primary_key=True)
    blob_id = Column(ForeignKey("blob.id"), primary_key=True)
    order = Column(Integer, index=True, default=None)
    type = Column(String(20), index=True, default=None)

    shot = relationship("Shot", back_populates="blobs")
    blob = relationship("Blob", back_populates="shots")


class Blob(Base, TimestamedTable):
    __tablename__ = "blob"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    url = Column(String(1000))
    sha256 = Column(String(64), unique=True)
    type = Column(String(20), index=True)

    shots = relationship("ShotBlob", back_populates="blob")


class Shot(Base, TimestamedTable):
    __tablename__ = "shot"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    custom = Column(String(50), index=True, default=None)
    status = Column(String(20), default=None)
    description = Column(String(100), default=None)

    blobs = relationship(
        "ShotBlob", back_populates="shot", order_by=lambda: asc(ShotBlob.order)
    )

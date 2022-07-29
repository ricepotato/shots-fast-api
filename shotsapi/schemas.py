from enum import Enum
from pydantic import BaseModel


class BlobType(str, Enum):
    main = "main"
    thumbnail = "thumbnail"


class BlobBase(BaseModel):
    name: str
    url: str
    type: BlobType
    order: int = 0


class ShotBase(BaseModel):
    name: str


class Blob(BlobBase):
    id: int = None

    class Config:
        orm_mode = True


class Shot(ShotBase):
    id: int = None
    images: list[Blob] = []

    class Config:
        orm_mode = True

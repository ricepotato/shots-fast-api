from enum import Enum
from pydantic import BaseModel


class BlobType(str, Enum):
    main = "main"
    thumbnail = "thumbnail"


class ShotStatus(str, Enum):
    present = "present"
    absent = "absent"


class BlobBase(BaseModel):
    name: str
    url: str
    type: BlobType
    order: int = 0


class Blob(BlobBase):
    id: int = None

    class Config:
        orm_mode = True


class ShotBase(BaseModel):
    name: str
    custom: str = None
    status: ShotStatus = None
    description: str = None


class Shot(ShotBase):
    id: int = None
    images: list[Blob] = []

    class Config:
        orm_mode = True


class ShotsResponse(BaseModel):
    page: int
    per_page: int
    data: list[Shot]

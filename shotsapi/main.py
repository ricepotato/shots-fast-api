from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from sqlalchemy import orm

import database
import crud

engine = database.create_engine()
SessionLocal = database.session_local(engine)


class Blob(BaseModel):
    name: str
    url: HttpUrl


class ShotResponse(BaseModel):
    name: str
    images: list[Blob]


class ShotsResponse(BaseModel):
    page: int = 1
    limit: int = 10
    data: list[ShotResponse] = []


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "hello"}


# @app.get("/shots/", response_model=ShotsResponse)
# async def get_shots():
#     return ShotsResponse(page=1, limit=10, data=data)


@app.get("/shots/{name}", response_model=ShotResponse)
async def get_shot(name: str, db: orm.Session = Depends(get_db)):
    shot = crud.get_shot_by_name(db, name)
    return ShotResponse(name=shot.name, images=shot.images)


@app.post("/shots/")
async def create_shot(shot: ShotResponse):
    return shot

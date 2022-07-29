from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from fastapi.middleware.cors import CORSMiddleware


class Blob(BaseModel):
    name: str
    url: HttpUrl


class Shot(BaseModel):
    name: str
    images: list[Blob]
    thumbnails: list[Blob]


class ShotResponse(BaseModel):
    page: int = 1
    limit: int = 10
    data: list[Shot] = []


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


"https://storage.googleapis.com/yazzal/6ba6986c98a7cc15a96d7b527fdb112219c21207e932846dcd5b719d368446fd"
"https://storage.googleapis.com/yazzal/7beb1a2c56d977fac450f8a26e69b4e496ec2b5a0a093aee07ee18429bd78f0e"

test_shot = Shot(
    name="shot1",
    images=[
        Blob(
            name="6ba6986c98a7cc15a96d7b527fdb112219c21207e932846dcd5b719d368446fd",
            url="https://storage.googleapis.com/yazzal/6ba6986c98a7cc15a96d7b527fdb112219c21207e932846dcd5b719d368446fd",
        )
    ],
    thumbnails=[
        Blob(
            name="7beb1a2c56d977fac450f8a26e69b4e496ec2b5a0a093aee07ee18429bd78f0e",
            url="https://storage.googleapis.com/yazzal/7beb1a2c56d977fac450f8a26e69b4e496ec2b5a0a093aee07ee18429bd78f0e",
        ),
    ],
)

data = [test_shot]


@app.get("/")
async def root():
    return {"message": "hello"}


@app.get("/shots/", response_model=ShotResponse)
async def get_shots():
    return ShotResponse(page=1, limit=10, data=data)


@app.get("/shots/{name}")
async def get_shot(name: str):
    return test_shot

from sqlalchemy.orm import Session

from .models import Blob as BlobModel, Shots as ShotsModel
from .schemas import Blob, Shot


def create_blob(db: Session, blob: Blob) -> int:
    new_blob = BlobModel(
        name=blob.name,
        url=blob.url,
        order=blob.order,
        type=blob.type,
    )
    db.add(new_blob)
    db.commit()
    db.flush()
    return new_blob.id


def create_shot(db: Session, shot: Shot):
    new_shot = ShotsModel(
        name=shot.name,
        images=[
            BlobModel(
                name=blob.name,
                url=blob.url,
                order=blob.order,
                type=blob.type,
            )
            for blob in shot.images
        ],
    )
    db.add(new_shot)
    db.commit()
    db.flush()
    return new_shot.id


def get_blob(db: Session, blob_id: int) -> BlobModel:
    return db.query(BlobModel).filter(BlobModel.id == blob_id).one()


def get_shot(db: Session, shot_id: int) -> ShotsModel:
    return db.query(ShotsModel).filter(ShotsModel.id == shot_id).one()

import hashlib
from sqlalchemy.orm import Session
import models

# from schemas import Blob, Shot, BlobType
import schemas


def get_sha256(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def create_blob(db: Session, blob: schemas.Blob) -> int:
    new_blob = models.Blob(
        name=blob.name, url=blob.url, sha256=get_sha256(blob.url), type=blob.type
    )
    db.add(new_blob)
    db.commit()
    db.flush()
    return new_blob.id


def create_shot(db: Session, shot: schemas.Shot):

    new_shot = models.Shot(
        name=shot.name,
        status=shot.status,
        description=shot.description,
        # images=[
        #     models.Blob(
        #         name=blob.name,
        #         url=blob.url,
        #         type=blob.type,
        #         sha256=get_sha256(blob.url),
        #     )
        #     for blob in shot.images
        # ],
    )

    for idx, blob in enumerate(shot.images):
        sb = models.ShotBlob(order=idx, type=schemas.BlobType.main)
        sb.blob = models.Blob(
            name=blob.name,
            url=blob.url,
            type=blob.type,
            sha256=get_sha256(blob.url),
        )
        new_shot.blobs.append(sb)

    for idx, blob in enumerate(shot.thumbnailes):
        sb = models.ShotBlob(order=idx, type=schemas.BlobType.thumbnail)
        sb.blob = models.Blob(
            name=blob.name,
            url=blob.url,
            type=blob.type,
            sha256=get_sha256(blob.url),
        )
        new_shot.blobs.append(sb)

    db.add(new_shot)
    db.commit()
    db.flush()
    return new_shot.id


def get_blob(db: Session, blob_id: int) -> models.Blob:
    return db.query(models.Blob).filter(models.Blob.id == blob_id).one()


def get_shot(db: Session, shot_id: int) -> models.Shot:
    return db.query(models.Shot).filter(models.Shot.id == shot_id).one()


def get_shot_by_name(db: Session, name: str) -> models.Shot:
    return db.query(models.Shot).filter(models.Shot.name == name).one()


def get_shot_list(db: Session, page: int, per_page: int) -> list[models.Shot]:
    return db.query(models.Shot).offset((page - 1) * per_page).limit(per_page).all()

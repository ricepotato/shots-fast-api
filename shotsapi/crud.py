from sqlalchemy.orm import Session

from models import Blob as BlobModel
from schemas import Blob


def get_blob(db: Session, blob_id: int):
    return db.query(BlobModel).filter(BlobModel.id == blob_id).one()


def create_blob(db: Session, blob: Blob):
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

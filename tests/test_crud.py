import pydantic
import pytest
from faker import Faker
from sqlalchemy.orm import Session
from shotsapi.crud import create_blob, create_shot, get_blob, get_shot
from shotsapi.schemas import Blob, BlobType, Shot

faker = Faker()


def test_create_blob_required_field_error():
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        # required field type
        Blob(name="blob_name", url=faker.url())

    with pytest.raises(pydantic.error_wrappers.ValidationError):
        # required field name
        Shot()


def test_create_blob(sqlite_session_local: Session):

    # given
    new_blob = Blob(name="blob_name", url=faker.url(), type=BlobType.main)
    blob_id = create_blob(sqlite_session_local, new_blob)
    assert blob_id

    # when
    blob = get_blob(sqlite_session_local, blob_id)

    # then
    assert blob.id == blob_id
    assert blob.url == new_blob.url
    assert blob.name == new_blob.name
    assert blob.type == new_blob.type


def test_create_shot(sqlite_session_local: Session):
    new_blob1 = Blob(name="blob_name1", url=faker.url(), type=BlobType.main)
    new_blob2 = Blob(name="blob_name2", url=faker.url(), type=BlobType.main)
    new_shot = Shot(name="shot1", images=[new_blob1, new_blob2])
    shot_id = create_shot(sqlite_session_local, new_shot)
    assert shot_id


def test_get_blob(sqlite_session_local: Session):
    new_blob = Blob(name="blob_name", url=faker.url(), type=BlobType.main)
    blob_id = create_blob(sqlite_session_local, new_blob)
    assert blob_id
    blob = get_blob(sqlite_session_local, blob_id)
    assert blob.name == "blob_name"


def test_get_shot(sqlite_session_local: Session):
    new_blob1 = Blob(name="blob_name1", url=faker.url(), type=BlobType.main)
    new_blob2 = Blob(name="blob_name2", url=faker.url(), type=BlobType.main)
    new_shot = Shot(name="shot1", images=[new_blob1, new_blob2])
    shot_id = create_shot(sqlite_session_local, new_shot)
    assert shot_id

    shot = get_shot(sqlite_session_local, shot_id)
    assert shot.name == "shot1"
    assert "blob_name1" in [blob.name for blob in shot.images]
    assert "blob_name2" in [blob.name for blob in shot.images]

import pydantic
import pytest
from faker import Faker
from sqlalchemy.orm import Session
from shotsapi import crud
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
    blob_id = crud.create_blob(sqlite_session_local, new_blob)
    assert blob_id

    # when
    blob = crud.get_blob(sqlite_session_local, blob_id)

    # then
    assert blob.id == blob_id
    assert blob.url == new_blob.url
    assert blob.name == new_blob.name
    assert blob.type == new_blob.type


def test_create_shot(sqlite_session_local: Session):
    new_blob1 = Blob(name="blob_name1", url=faker.url(), type=BlobType.main)
    new_blob2 = Blob(name="blob_name2", url=faker.url(), type=BlobType.main)
    new_blob3 = Blob(name="blob_name3", url=faker.url(), type=BlobType.main)
    new_shot = Shot(
        name="shot1",
        images=[new_blob2, new_blob1],
        thumbnailes=[
            new_blob3,
        ],
    )
    shot_id = crud.create_shot(sqlite_session_local, new_shot)
    assert shot_id

    shot = crud.get_shot(sqlite_session_local, shot_id)
    assert shot.blobs[0].blob.name == "blob_name2"


def test_get_blob(sqlite_session_local: Session):
    new_blob = Blob(name="blob_name", url=faker.url(), type=BlobType.main)
    blob_id = crud.create_blob(sqlite_session_local, new_blob)
    assert blob_id
    blob = crud.get_blob(sqlite_session_local, blob_id)
    assert blob.name == "blob_name"


def test_get_shot(sqlite_session_local: Session):
    new_blob1 = Blob(name="blob_name1", url=faker.url(), type=BlobType.main)
    new_blob2 = Blob(name="blob_name2", url=faker.url(), type=BlobType.main)
    new_shot = Shot(name="shot1", images=[new_blob1, new_blob2])
    shot_id = crud.create_shot(sqlite_session_local, new_shot)
    assert shot_id

    shot = crud.get_shot(sqlite_session_local, shot_id)
    assert shot.name == "shot1"
    # assert "blob_name1" in [blob.name for blob in shot.images]
    # assert "blob_name2" in [blob.name for blob in shot.images]


def test_get_shot_list(sqlite_session_local: Session):
    # given
    new_shot1 = Shot(name="shot1")
    new_shot2 = Shot(name="shot2")

    crud.create_shot(sqlite_session_local, new_shot1)
    crud.create_shot(sqlite_session_local, new_shot2)

    # when
    result1 = crud.get_shot_list(sqlite_session_local, 1, 10)
    result2 = crud.get_shot_list(sqlite_session_local, 1, 1)
    result3 = crud.get_shot_list(sqlite_session_local, 2, 1)

    # then
    assert result1[0].name == new_shot1.name
    assert result1[1].name == new_shot2.name
    assert result2[0].name == new_shot1.name
    assert result3[0].name == new_shot2.name


def test_get_shot_by_name(sqlite_session_local: Session):
    # given
    new_shot1 = Shot(name="shot1")
    new_shot2 = Shot(name="shot2")

    crud.create_shot(sqlite_session_local, new_shot1)
    crud.create_shot(sqlite_session_local, new_shot2)

    # when
    result1 = crud.get_shot_by_name(sqlite_session_local, name="shot1")

    # then
    assert result1.name == "shot1"


def test_shots_blobs_association(sqlite_session_local: Session):
    # given
    new_shot1 = Shot(name="shot1")
    new_shot2 = Shot(name="shot2")

    new_blob1 = Blob(name="blob_name1", url=faker.url(), type=BlobType.main)
    new_blob2 = Blob(name="blob_name2", url=faker.url(), type=BlobType.main)

    new_shot1.images.append(new_blob1)
    new_shot1.images.append(new_blob2)

    crud.create_shot(sqlite_session_local, new_shot1)
    crud.create_shot(sqlite_session_local, new_shot2)

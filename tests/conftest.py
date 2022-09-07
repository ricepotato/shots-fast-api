import os

import pytest
from shotsapi.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def remove_if_exists(path: str):
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def sqlite_db():
    sqlite_db_filepath = "db.sqlite"
    remove_if_exists(sqlite_db_filepath)
    engine = create_engine(f"sqlite:///{sqlite_db_filepath}", echo=True)
    Base.metadata.create_all(bind=engine)

    yield engine

    # remove_if_exists(sqlite_db_filepath)


@pytest.fixture
def sqlite_session_local(sqlite_db) -> Session:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_db)
    session = SessionLocal()
    yield session
    session.close()

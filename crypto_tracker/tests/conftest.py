import pytest
from typing import Generator

from crypto_tracker.database import SessionLocal, Base, engine


@pytest.fixture(autouse=True)
def initdb():
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def db() -> Generator:
    yield SessionLocal()
from sqlalchemy.orm import Session

from crypto_tracker import crud
from crypto_tracker.schemas import UserCreate
from crypto_tracker.tests.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    user = UserCreate(email=email, password=random_lower_string(12))
    crud.create_user(db, user)

    db_user = crud.get_user_by_email(db, email=email)
    assert db_user is not None
    assert db_user.email == email
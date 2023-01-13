from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud, schemas


router = APIRouter(tags=["users"])


# required function until autorization will be implemented (only for testing)
@router.get("/users", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(404, "Email has not registered")

    return user


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(400, "Email already registered")

    return crud.create_user(db, user)



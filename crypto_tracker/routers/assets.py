from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud, schemas

router = APIRouter(tags=["assets"])


@router.post("/users/{user_id}/portfolios/{portfolio_id}/", response_model=schemas.Asset)
def create_asset(asset: schemas.AssetCreate, user_id: int, portfolio_id: int, db: Session = Depends(get_db)):
    db_asset = crud.create_asset(db, asset, portfolio_id)
    if db_asset is None:
        raise HTTPException(400, "Asset already exists.")

    return db_asset


@router.patch("/users/{user_id}/portfolios/{portfolio_id}/", response_model=schemas.Asset)
def update_asset(asset: schemas.AssetUpdate, portfolio_id: int, db: Session = Depends(get_db)):
    db_asset = crud.update_asset(db, asset, portfolio_id)
    if db_asset is None:
        raise HTTPException(404, "Not found")

    return db_asset


@router.delete("/users/{user_id}/portfolios/{portfolio_id}/assets/{asset_id}/")
def delete_asset(user_id: int, portfolio_id: int, asset_id: int, db: Session = Depends(get_db)):
    return crud.delete_asset(db, portfolio_id, asset_id)
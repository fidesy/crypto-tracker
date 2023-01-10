from sqlalchemy.orm import Session
from typing import Union

from .. import models, schemas


def create_asset(db: Session, asset: schemas.AssetCreate, portfolio_id: int) -> Union[models.Asset, None]:
    # get portfolio that has the same title and currency
    db_asset = db.query(models.Asset).filter(
        models.Asset.portfolio_id == portfolio_id, 
        models.Asset.currency_id == asset.currency_id).first()

    # if the asset already exists then raise an error
    if db_asset is not None:
        return None

    db_asset = models.Asset(**asset.dict(), portfolio_id=portfolio_id)
    db.add(db_asset)    
    db.commit()
    db.refresh(db_asset)
    return db_asset


def update_asset(db: Session, asset: schemas.AssetUpdate, portfolio_id: int) -> Union[models.Asset, None]:
    db_asset = db.query(models.Asset).filter(models.Asset.portfolio_id == portfolio_id, models.Asset.id == asset.id).first()
    if db_asset is None:
        return None

    db_asset.amount = asset.amount
    db.commit()
    db.refresh(db_asset)
    return db_asset


def delete_asset(db: Session, portfolio_id: int, asset_id: int) -> int:
    status = db.query(models.Asset).filter(models.Asset.portfolio_id == portfolio_id, models.Asset.id == asset_id).delete()
    db.commit()
    return status
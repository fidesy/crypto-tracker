from sqlalchemy.orm import Session

from . import models, schemas


def get_curencies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Currency).offset(skip).limit(limit).all()


def get_candlesticks(db: Session, symbol: str):
    return db.query(models.Candlestick).filter(models.Candlestick.symbol == symbol).order_by(models.Candlestick.date.desc()).limit(200).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

    
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_portfolio_by_user_id(db: Session, user_id: int):
    return db.query(models.Portfolio).filter(models.Portfolio.user_id == user_id).all()


def create_portfolio_asset(db: Session, asset: schemas.PortfolioCreate, user_id: int):
    # get portfolio that has the same title and currency
    db_asset = db.query(models.Portfolio).filter(
        models.Portfolio.user_id == user_id, 
        models.Portfolio.title == asset.title,
        models.Portfolio.currency_id == asset.currency_id).first()

    # if there is no instance then creating a new
    if db_asset is None:
        db_asset = models.Portfolio(**asset.dict(), user_id=user_id)
        db.add(db_asset)
    else:
        db_asset.amount += asset.amount
    
    db.commit()
    db.refresh(db_asset)
    return db_asset


def update_portfolio_asset(db: Session, asset: schemas.Portfolio):
    db_asset = db.query(models.Portfolio).filter(models.Portfolio.id == asset.id).first()
    if db_asset is None:
        return None

    db_asset.amount = asset.amount
    db.commit()
    db.refresh(db_asset)
    return db_asset


def delete_portfolio_asset(db: Session, portfolio_id: int):
    status = db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).delete()
    db.commit()
    return status

    

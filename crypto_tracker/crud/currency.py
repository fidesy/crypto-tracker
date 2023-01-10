from sqlalchemy.orm import Session

from .. import models, schemas


def create_currency(db: Session, currency: schemas.CurrencyCreate) -> models.Currency:
    db_currency = models.Currency(**currency.dict())
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency


def get_currencies(db: Session, skip: int = 0, limit: int = 100) -> list[models.Currency]:
    currencies = db.query(models.Currency).offset(skip).limit(limit).all()
    # get price for each currency
    for ind in range(len(currencies)):
        candlestick = db.query(models.Candlestick).filter(models.Candlestick.symbol == currencies[ind].symbol).order_by(models.Candlestick.date.desc()).limit(1).first()
        if candlestick is None:
            continue
        
        currencies[ind].price = candlestick.close

    return currencies


def get_candlesticks(db: Session, symbol: str, skip: int = 0, limit: int = 200) -> list[models.Candlestick]:
    return db.query(models.Candlestick).filter(models.Candlestick.symbol == symbol).order_by(models.Candlestick.date.desc()).offset(skip).limit(limit).all()
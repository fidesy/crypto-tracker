from sqlalchemy.orm import Session

from .. import models, schemas


def get_portfolios_by_user_id(db: Session, user_id: int) -> list[models.Portfolio]:
    return db.query(models.Portfolio).filter(models.Portfolio.user_id == user_id).all()


def get_portfolio(db: Session, user_id: int, portfolio_id: int) -> models.Portfolio:
    return db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()


def create_portfolio(db: Session, portfolio: schemas.Portfolio, user_id: int) -> models.Portfolio:
    title = portfolio.title.lower()
    db_portfolio = models.Portfolio(title=title, user_id=user_id)
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio


def delete_portfolio(db: Session, user_id: int, portfolio_id: int) -> int:
    # delete all assets from the portfolio
    db.query(models.Asset).filter(models.Asset.portfolio_id == portfolio_id).delete()
    
    status = db.query(models.Portfolio).filter(models.Portfolio.user_id == user_id, models.Portfolio.id == portfolio_id).delete()
    db.commit()
    return status


def get_portfolio_prices(db: Session, user_id: int, portfolio_id: int):
    assets = db.query(models.Asset).filter(models.Asset.portfolio_id == portfolio_id).all()
    prices = {}
    for asset in assets:
        candlesticks = db.query(models.Candlestick).filter(models.Candlestick.symbol == asset.currency.symbol).all()
        for candle in candlesticks:
            if candle.date not in prices:
                prices[candle.date] = 0

            prices[candle.date] += asset.amount*candle.close

    return [{"date": k, "close": v} for k, v in prices.items()]
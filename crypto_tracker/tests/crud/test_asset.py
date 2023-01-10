from sqlalchemy.orm import Session

from crypto_tracker.schemas import AssetCreate, AssetUpdate, CurrencyCreate, UserCreate, PortfolioCreate
from crypto_tracker import crud
from crypto_tracker.tests.utils import random_email, random_lower_string



def test_init_params(db: Session):
    global user_id, portfolio_id, currency_id
    user_id = crud.create_user(db, UserCreate(email=random_email(), password=random_lower_string(12))).id
    
    portfolio_id = crud.create_portfolio(db, PortfolioCreate(title=random_lower_string(10)), user_id).id
    
    currency_id = crud.create_currency(db, CurrencyCreate(
        name=random_lower_string(6),
        symbol=random_lower_string(6),
        image_url=random_lower_string(20))).id


def test_create_asset(db: Session):
    amount = 1
    asset = AssetCreate(currency_id=currency_id, amount=amount)
    crud.create_asset(db, asset, portfolio_id)

    portfolio = crud.get_portfolio(db, user_id, portfolio_id)
    assert len(portfolio.assets) == 1
    assert portfolio.assets[0].currency_id == currency_id
    assert portfolio.assets[0].amount == amount


def test_update_asset(db: Session):
    assets = crud.get_portfolio(db, user_id, portfolio_id).assets
    assert len(assets) == 1

    amount = 5
    crud.update_asset(db, 
        AssetUpdate(currency_id=currency_id, amount=amount, id=assets[0].id), 
        portfolio_id)

    assets = crud.get_portfolio(db, user_id, portfolio_id).assets
    assert len(assets) == 1
    assert assets[0].amount == amount


def test_delete_asset(db: Session):
    assets = crud.get_portfolio(db, user_id, portfolio_id).assets
    assert len(assets) == 1

    crud.delete_asset(db, portfolio_id, assets[0].id)

    assets = crud.get_portfolio(db, user_id, portfolio_id).assets
    assert len(assets) == 0

from sqlalchemy.orm import Session

from crypto_tracker.schemas import PortfolioCreate, UserCreate
from crypto_tracker import crud
from crypto_tracker.tests.utils import random_email, random_lower_string


def test_create_portfolio(db: Session):
    # create user to obtain a new user_id
    global user_id
    user_id = crud.create_user(db, UserCreate(email=random_email(), password=random_lower_string(12))).id

    portfolio = PortfolioCreate(title="Test")
    crud.create_portfolio(db, portfolio, user_id=user_id)

    portfolios = crud.get_portfolios_by_user_id(db, user_id)
    assert len(portfolios) == 1
    assert portfolios[0].title == "test"


def test_get_portfolio(db: Session):
    portfolios = crud.get_portfolios_by_user_id(db, user_id)
    portfolio = crud.get_portfolio(db, user_id, portfolios[0].id)
    
    assert portfolio is not None
    assert portfolio.title == "test"
    assert len(portfolio.assets) == 0


def delete_portfolio(db: Session):
    portfolios = crud.get_portfolios_by_user_id(db, user_id)
    assert len(portfolios) == 1

    crud.delete_portfolio()

    portfolios_new = crud.get_portfolios_by_user_id(db, user_id)
    assert len(portfolios_new) == 0
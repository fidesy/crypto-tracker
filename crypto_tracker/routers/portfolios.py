from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud, schemas



router = APIRouter(tags=["portfolio"])


@router.get("/users/{user_id}/portfolios/", response_model=list[schemas.Portfolio])
def get_portfolios(user_id: int, db: Session = Depends(get_db)):
    return crud.get_portfolios_by_user_id(db, user_id)


@router.get("/users/{user_id}/portfolios/{portfolio_id}/", response_model=schemas.Portfolio)
def get_portfolio(user_id: int, portfolio_id: int, db: Session = Depends(get_db)):
    portfolio = crud.get_portfolio(db, user_id, portfolio_id)
    if portfolio is None:
        raise HTTPException(404, "Portfolio not found.")

    return portfolio


@router.post("/users/{user_id}/portfolios/", response_model=schemas.Portfolio)
def create_portfolio(portfolio: schemas.PortfolioCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_portfolio(db, portfolio, user_id)


@router.patch("/users/{user_id}/portfolios/{portfolio_id}")
def update_portfolio(user_id: int, portfolio_id: int):
    ...


@router.delete("/users/{user_id}/portfolios/{portfolio_id}")
def delete_portfolio(user_id: int, portfolio_id: int, db: Session = Depends(get_db)):
    return crud.delete_portfolio(db, user_id, portfolio_id)


# response model include date and close price
@router.get("/users/{user_id}/portfolios/{portfolio_id}/prices")
def get_portfolio_prices(user_id: int, portfolio_id: int, db: Session = Depends(get_db)):
    return crud.get_portfolio_prices(db, user_id, portfolio_id)
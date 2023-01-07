from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(400, "Email already registered")

    return crud.create_user(db, user)


@app.get("/users/{user_id}/portfolio/", response_model=list[schemas.Portfolio])
def get_portfolio(user_id: int, db: Session = Depends(get_db)):
    return crud.get_portfolio_by_user_id(db, user_id)


@app.post("/users/{user_id}/portfolio/", response_model=schemas.Portfolio)
def create_portfolio_asset(portfolio: schemas.PortfolioCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_portfolio_asset(db, portfolio, user_id)


@app.patch("/users/{user_id}/portfolio/", response_model=schemas.Portfolio)
def update_portfolio_asset(asset: schemas.PortfolioUpdate, db: Session = Depends(get_db)):
    db_asset = crud.update_portfolio_asset(db, asset)
    if db_asset is None:
        raise HTTPException(404, "Not found")

    return db_asset


@app.delete("/users/{user_id}/portfolio/{portfolio_id}")
def delete_portfolio_asset(user_id: int, portfolio_id: int, db: Session = Depends(get_db)):
    return crud.delete_portfolio_asset(db, portfolio_id)


# response model include date and close price
@app.get("/users/{user_id}/portfolio/{portfolio_title}/")
def get_portfolio_prices(user_id: int, portfolio_title: str, db: Session = Depends(get_db)):
    return crud.get_portfolio_prices(db, user_id, portfolio_title)


@app.get("/currencies/", response_model=list[schemas.Currency])
def get_currencies(db: Session = Depends(get_db)):
    return crud.get_curencies(db)
  

@app.get("/klines/{symbol}/", response_model=list[schemas.Candlestick])
def get_candlesticks(symbol: str , db: Session = Depends(get_db)):
    return crud.get_candlesticks(db, symbol)
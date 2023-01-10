from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import crud, schemas


router = APIRouter(tags=["currencies"])


@router.get("/currencies/", response_model=list[schemas.Currency])
def get_currencies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_currencies(db, skip, limit)
  

@router.get("/klines/{symbol}/", response_model=list[schemas.Candlestick])
def get_candlesticks(symbol: str, skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    return crud.get_candlesticks(db, symbol, skip, limit)
from fastapi import APIRouter

from . import assets, currencies, portfolios, users

router = APIRouter()

router.include_router(assets.router)
router.include_router(currencies.router)
router.include_router(portfolios.router)
router.include_router(users.router)
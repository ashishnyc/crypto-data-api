from datetime import datetime, date
from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.db_setup import get_session
from routers import Constants as cs

router = APIRouter()


@router.post("/bybit/markets/perpetual/info", tags=[cs.Tags.process["name"]])  # type: ignore
def process_uploaded_perpetual_market_info(
    downloaded_before: datetime = None,  # type: ignore
    session: Session = Depends(get_session),
):
    pass


@router.post("/bybit/markets/spot/info", tags=[cs.Tags.process["name"]])  # type: ignore
def process_uploaded_spot_market_info(
    downloaded_before: datetime = None,  # type: ignore
    session: Session = Depends(get_session),
):
    pass

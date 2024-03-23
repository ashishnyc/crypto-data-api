from datetime import datetime, date
from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.db_setup import get_session
from routers import Constants as cs
from db import operations as ops

router = APIRouter()


@router.post("/bybit/markets/perpetual/info", tags=[cs.Tags.upload["name"]])  # type: ignore
async def bybit_upload_perpetual_market_info(
    symbol: cs.ByBitTables.PerpDaily,
    session: Session = Depends(get_session),
):
    dt = datetime.now().replace(microsecond=0, minute=0, second=0)
    symbol.downloaded_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    session.add(symbol)
    session.commit()
    session.refresh(symbol)
    return "Success"


@router.post("/bybit/markets/spot/info", tags=[cs.Tags.upload["name"]])  # type: ignore
async def bybit_upload_spot_market_info(
    symbol: cs.ByBitTables.SpotDaily,
    session: Session = Depends(get_session),
):
    dt = datetime.now().replace(microsecond=0, minute=0, second=0)
    symbol.downloaded_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    session.add(symbol)
    session.commit()
    session.refresh(symbol)
    return symbol


@router.post("/bybit/perpetual/kline/download/schedule/{symbol}", tags=[cs.Tags.upload["name"]])  # type: ignore
async def upload_bybit_perpetual_kline_download_schedule(
    symbol: str,
    kline_date: date = None,  # type: ignore
    session: Session = Depends(get_session),
):
    return ops.create_perp_kline_schedule(
        symbol=symbol, kline_date=kline_date, session=session
    )

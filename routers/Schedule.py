from datetime import date
from enum import Enum

from fastapi import APIRouter, Depends
from sqlmodel import Session, select, not_

from db import operations as ops
from db.db_setup import get_session
from db.models import Symbols, Klines

router = APIRouter()


class Table:
    Perp = Symbols.BBPerpetualSymbols
    Spot = Symbols.BBSpotSymbols
    PerpDaily = Symbols.BBPerpetualSymbolsDaily
    SpotDaily = Symbols.BBSpotSymbolsDaily
    PerpSchedule = Klines.ByBitPerpetualKlineDownloadSchedule
    # SpotSchedule = Klines.ByBitSpotKlineDownloadSchedule


class Tags(str, Enum):
    perp = "Perpetual"
    spot = "Spot"


@router.get(
    "/kline/perp",
    tags=[Tags.perp],
    response_model=list[Klines.ByBitPerpetualKlineDownloadSchedule],
)
async def get_kline_perp_schedule(
    limit: int = 200,
    session: Session = Depends(get_session),
):
    limit = min(limit, 200)
    tbl_schedule = Table.PerpSchedule
    stmt = select(tbl_schedule).where(not_(tbl_schedule.is_downloaded))
    stmt = stmt.limit(limit)
    result = session.exec(stmt)
    schedules = result.all()
    return schedules


@router.post("/kline/perp/{symbol}", tags=[Tags.perp])
async def get_kline_perp_symbol_schedule(
    symbol: str,
    session: Session = Depends(get_session),
):
    return ops.create_perp_kline_schedule(symbol=symbol, session=session)


@router.post("/kline/perp/{symbol}/{kline_date}", tags=[Tags.perp])
async def get_kline_perp_symbol_kline_date_schedule(
    symbol: str,
    kline_date: date,
    session: Session = Depends(get_session),
):
    return ops.create_perp_kline_schedule(
        symbol=symbol, kline_date=kline_date, session=session
    )


@router.post("/kline/perp/update", tags=[Tags.perp])
async def update_kline_perp_symbol_kline_date_schedule(
    schedule: Klines.ByBitPerpetualKlineDownloadSchedule,
    session: Session = Depends(get_session),
):
    tbl_schedule = Klines.ByBitPerpetualKlineDownloadSchedule
    old_schedule = session.exec(
        select(tbl_schedule).where(tbl_schedule.id == schedule.id)
    ).one_or_none()
    old_schedule.is_downloaded = schedule.is_downloaded  # type: ignore
    old_schedule.error = schedule.error  # type: ignore
    session.add(old_schedule)
    session.commit()
    session.refresh(old_schedule)
    return old_schedule

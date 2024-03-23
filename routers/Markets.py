from fastapi import APIRouter, Depends
from sqlmodel import Session, select, not_

from db.db_setup import get_session
from routers import Constants as cs

router = APIRouter()


@router.get("/bybit/perpetual/symbols", tags=[cs.Tags.markets["name"]])
async def get_bybit_perpetual_symbols(
    symbol: str = None,  # type: ignore
    session: Session = Depends(get_session),
):
    perp_stmt = select(cs.ByBitTables.Perp)
    if symbol:
        perp_stmt = perp_stmt.where(cs.ByBitTables.Perp.symbol == symbol)
    result = session.exec(perp_stmt)
    symbols = result.all()
    return symbols


@router.get("/bybit/perpetual/klines", tags=[cs.Tags.markets["name"]])
async def get_bybit_perpetual_klines(
    symbol: str = None,  # type: ignore
    kline_date: str = None,  # type: ignore
    session: Session = Depends(get_session),
):
    pass


@router.get("/bybit/spot/symbols", tags=[cs.Tags.markets["name"]])
async def get_bybit_spot_symbols(
    symbol: str = None,  # type: ignore
    session: Session = Depends(get_session),
):
    spot_stmt = select(cs.ByBitTables.Spot)
    if symbol:
        spot_stmt = spot_stmt.where(cs.ByBitTables.Spot.symbol == symbol)
    result = session.exec(spot_stmt)
    symbols = result.all()
    return symbols


@router.get("/bybit/spot/klines", tags=[cs.Tags.markets["name"]])
async def get_bybit_spot_klines(
    symbol: str = None,  # type: ignore
    kline_date: str = None,  # type: ignore
    session: Session = Depends(get_session),
):
    pass


@router.get("/bybit/perpetual/kline/download/schedule", tags=[cs.Tags.markets["name"]])
async def get_bybit_perpetual_kline_download_schedule(
    symbol: str = None,  # type: ignore
    limit: int = 200,
    session: Session = Depends(get_session),
):
    limit = min(limit, 200)
    tbl_schedule = cs.ByBitTables.PerpSchedule
    stmt = select(tbl_schedule)
    stmt = stmt.where(not_(tbl_schedule.is_downloaded))
    stmt = stmt.limit(limit)
    result = session.exec(stmt)
    schedules = result.all()
    return schedules


@router.put("/bybit/perpetual/kline/download/schedule", tags=[cs.Tags.markets["name"]])
async def put_bybit_perpetual_kline_download_schedule(
    symbol: str,
    session: Session = Depends(get_session),
):
    pass


@router.delete(
    "/bybit/perpetual/kline/download/schedule", tags=[cs.Tags.markets["name"]]
)
async def delete_bybit_perpetual_kline_download_schedule(
    symbol: str = None,  # type: ignore
    session: Session = Depends(get_session),
):
    pass


@router.get("/bybit/spot/kline/download/schedule", tags=[cs.Tags.markets["name"]])
async def get_bybit_spot_kline_download_schedule(
    symbol: str = None,  # type: ignore
    session: Session = Depends(get_session),
):
    pass


@router.put("/bybit/spot/kline/download/schedule", tags=[cs.Tags.markets["name"]])
async def put_bybit_spot_kline_download_schedule(
    symbol: str = None,  # type: ignore
    session: Session = Depends(get_session),
):
    pass


@router.delete("/bybit/spot/kline/download/schedule", tags=[cs.Tags.markets["name"]])
async def delete_bybit_spot_kline_download_schedule(
    symbol: str = None,  # type: ignore
    session: Session = Depends(get_session),
):
    pass

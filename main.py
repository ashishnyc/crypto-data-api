import logging
import sys
from datetime import date, datetime

import uvicorn
from fastapi import Depends, FastAPI
from sqlmodel import Session, select

import utils
from db import db_setup
from db import operations as ops
from db.db_setup import get_session
from db.models import Klines, Symbols

logger = utils.get_logger(logging.getLogger())
app = FastAPI()


@app.get("/symbols/all", response_model=list[Symbols.BBPerpetualSymbolsDaily])
def get_symbols(
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
    result = session.exec(select(Symbols.BBPerpetualSymbolsDaily))
    symbols = result.all()
    return symbols


@app.post("/symbols/perp")
def add_symbols(
    symbol: Symbols.BBPerpetualSymbolsDaily,
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
    # default value does not work
    dt = datetime.now().replace(microsecond=0, minute=0, second=0)
    symbol.downloaded_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    session.add(symbol)
    session.commit()
    session.refresh(symbol)
    return symbol


@app.post("/symbols/spot")
def add_spot_symbols(
    symbol: Symbols.BBSpotSymbolsDaily,
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
    dt = datetime.now().replace(microsecond=0, minute=0, second=0)
    symbol.downloaded_at = dt.strftime("%Y-%m-%d %H:%M:%S")
    session.add(symbol)
    session.commit()
    session.refresh(symbol)
    return symbol


@app.get("/process/raw-data")
def process_raw_data(
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
    ds = date.today().strftime("%Y-%m-%d")
    utils.process_perp_daily_data(session=session, ds=ds)
    utils.process_spot_daily_data(session=session, ds=ds)


@app.get("/produce/perp/klines-schedule")
def produce_perp_klines_schedule(
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
    tbl_symbol = Symbols.BBPerpetualSymbols
    perp_symbols_stmt = select(tbl_symbol)
    perp_symbols = session.exec(perp_symbols_stmt).all()
    for perp_symbol in perp_symbols:
        ops.create_perp_kline_schedule(
            symbol=perp_symbol.symbol, session=session)
    return "Kline Schedule Created"


@app.get("/produce/perp/klines-schedule/{symbol}")
def produce_perp_klines_schedule_for_symbol(
    symbol: str,
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
    return ops.create_perp_kline_schedule(symbol=symbol, session=session)


@app.get("/produce/perp/klines-schedule/{symbol}/{kline_date}")
def produce_perp_klines_schedule_for_symbol_and_date(
    symbol: str,
    kline_date: date,
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
    return ops.create_perp_kline_schedule(symbol=symbol, kline_date=kline_date, session=session)


if __name__ == "__main__":
    logger.info("Starting the app")
    db_setup.create_db_and_tables()
    args = utils.parse_arguments(sys.argv[1:])
    host, port = utils.get_host_and_port(env=args.env)
    uvicorn.run(app, host=host, port=port)

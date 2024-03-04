from datetime import date
import select
from fastapi import Depends, FastAPI
from sqlmodel import Session, select
import uvicorn
from db.db_setup import create_db_and_tables, get_session
from db.models import Symbols
import utils
import sys

app = FastAPI()


@app.get("/symbols/all", response_model=list[Symbols.BBPerpetualSymbolsDaily])
def get_symbols(
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
    result = session.exec(select(Symbols.BBPerpetualSymbolsDaily))
    symbols = result.all()
    return symbols


@app.post("/symbols/perpetual")
def add_symbols(
    symbol: Symbols.BBPerpetualSymbolsDaily,
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
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


if __name__ == "__main__":
    create_db_and_tables()
    args = utils.parse_arguments(sys.argv[1:])
    host, port = utils.get_host_and_port(env=args.env)
    uvicorn.run(app, host=host, port=port)

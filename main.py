import select
from fastapi import Depends, FastAPI
from sqlmodel import Session, select
import uvicorn
from db.db_setup import create_db_and_tables, get_session
from db.models import Symbols
import utils
import sys

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/symbols", response_model=list[Symbols.BBPerpetualSymbolsDaily])
def get_symbols(session: Session = Depends(get_session)):
    result = session.exec(select(Symbols.BBPerpetualSymbolsDaily))
    symbols = result.all()
    return symbols


@app.post("/symbols")
def add_symbols(
    symbol: Symbols.BBPerpetualSymbolsDaily,
    session: Session = Depends(get_session),
):
    session.add(symbol)
    session.commit()
    session.refresh(symbol)
    return symbol


@app.post("/symbols/spot")
def add_spot_symbols(
    symbol: Symbols.BBSpotSymbolsDaily,
    session: Session = Depends(get_session),
):
    session.add(symbol)
    session.commit()
    session.refresh(symbol)
    return symbol


if __name__ == "__main__":
    create_db_and_tables()
    args = utils.parse_arguments(sys.argv[1:])
    host, port = utils.get_host_and_port(env=args.env)
    uvicorn.run(app, host=host, port=port)

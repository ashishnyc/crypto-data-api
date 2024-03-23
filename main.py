import logging
import sys
from datetime import date, datetime

import uvicorn
from fastapi import Depends, FastAPI
from sqlmodel import Session, select, not_

import utils
from db import db_setup
from db import operations as ops
from db.db_setup import get_session
from db.models import Klines, Symbols
from routers import Schedule, Upload, Constants, Process, Markets

logger = utils.get_logger(logging.getLogger())
app = FastAPI(
    dependencies=[Depends(utils.authenticate_user)],
    openapi_tags=Constants.tags_metadata,
)

app.include_router(Upload.router, prefix="/upload")
app.include_router(Markets.router, prefix="/markets")
app.include_router(Process.router, prefix="/process")
app.include_router(Schedule.router, prefix="/schedule")


@app.get("/process/raw-data")
def process_raw_data(
    session: Session = Depends(get_session),
    username: str = Depends(utils.authenticate_user),
):
    ds = date.today().strftime("%Y-%m-%d")
    utils.process_perp_daily_data(session=session, ds=ds)
    utils.process_spot_daily_data(session=session, ds=ds)


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    logger.info("Starting the app")
    db_setup.create_db_and_tables()
    args = utils.parse_arguments(sys.argv[1:])
    host, port = utils.get_host_and_port(env=args.env)
    uvicorn.run(app, host=host, port=port)

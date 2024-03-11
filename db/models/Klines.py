from datetime import date
from operator import is_
from typing import Optional
from sqlmodel import Field, SQLModel, select, and_


class ByBitPerpetualKlineDownloadSchedule(SQLModel, table=True):
    __tablename__ = "bb_perp_kline_download_scheduler"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    kline_date: date
    is_downloaded: bool = Field(default=False)

    def is_exists(self, session):
        tbl = ByBitPerpetualKlineDownloadSchedule
        stmt = select(tbl).where(
            and_(tbl.symbol == self.symbol, tbl.kline_date == self.kline_date)
        )
        schedules = session.exec(stmt).all()
        return len(schedules) > 0

    def add_kline_schedule(self, session):
        if not self.is_exists(session):
            session.add(self)
            session.commit()
            session.refresh(self)
            return "Added"
        return "Already Exists"


class ByBitPerpetualKlineRaw(SQLModel, table=True):
    __tablename__ = "bb_perp_kline_raw"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    start_time: str = Field(default="0")
    open: str = Field(default="0")
    high: str = Field(default="0")
    low: str = Field(default="0")
    close: str = Field(default="0")
    volume: str = Field(default="0")
    turnover: str = Field(default="0")

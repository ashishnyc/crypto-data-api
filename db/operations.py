from datetime import date

from sqlmodel import Session, select

from db.models import Klines, Symbols


def create_perp_kline_schedule(session: Session, symbol: str, kline_date: date = date(1900, 1, 1)):
    dates = []
    tbl_symbol = Symbols.BBPerpetualSymbols
    if kline_date == date(1900, 1, 1):
        symbol_stmt = select(tbl_symbol).where(tbl_symbol.symbol == symbol)
        symbol_data = session.exec(symbol_stmt).one_or_none()
        dates.extend(symbol_data.get_dates_from_launch_time())  # type: ignore
    else:
        dates.append(kline_date)

    for kline_date in dates:
        tbl_perp_kline_schedule = Klines.ByBitPerpetualKlineDownloadSchedule
        kline = tbl_perp_kline_schedule(symbol=symbol, kline_date=kline_date)
        kline.add_kline_schedule(session=session)
    return "Kline Schedule Created"

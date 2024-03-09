import os
import argparse
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from db.models import Constants
from db.models import Symbols
from sqlmodel import select, func
from logtail import LogtailHandler
import logging

security = HTTPBasic()


def get_loggly_config_location() -> str:
    """
    Retrieves logging config file from env variable

    Returns:
        Logging File Location

    Raises:
        EnvironmentError
    """
    loggly_config_file = os.environ.get("LOGGLY_CONF_FILE")
    if not loggly_config_file:
        raise EnvironmentError("Missing logger file environment variable")
    return loggly_config_file


def parse_arguments(args: list):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--env",
        help="select environment to run",
        type=str,
        choices=["prod", "local"],
        default="local",
    )
    return parser.parse_args(args)


def get_host_and_port(env: str) -> tuple:
    if env == "local":
        return ("127.0.0.1", 1234)
    return ("0.0.0.0", 1234)


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, os.environ.get("DATA_API_USER", "")
    )
    correct_password = secrets.compare_digest(
        credentials.password, os.environ.get("DATA_API_PASS", "")
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def update_none_to_unknown(value: str) -> str:
    return value.upper().replace("NONE", Constants.UNKNOWN)


def process_perp_daily_data(session, ds):
    daily_tbl = Symbols.BBPerpetualSymbolsDaily
    ds_stmt = select(func.max(daily_tbl.downloaded_at).label("max_ds"))
    latest_ds = session.exec(ds_stmt).one_or_none()
    latest_snapshot = select(daily_tbl).where(daily_tbl.downloaded_at == latest_ds)
    ds_symbols = session.exec(latest_snapshot).all()
    for r in ds_symbols:
        stmt = select(Symbols.BBPerpetualSymbols)
        stmt = stmt.where(Symbols.BBPerpetualSymbols.symbol == r.symbol)
        new_or_old = session.exec(stmt).one_or_none()
        if new_or_old is None:
            new_or_old = Symbols.BBPerpetualSymbols(symbol=r.symbol)
        new_or_old.status = r.get_status()
        new_or_old.contract_type = r.get_contract_type()
        new_or_old.has_unified_margin_trade = r.get_has_unified_margin_trade()
        new_or_old.base_coin = r.get_base_coin()
        new_or_old.quote_coin = r.get_quote_coin()
        new_or_old.settle_coin = r.get_settle_coin()
        new_or_old.launch_time = r.get_launch_time()
        new_or_old.delivery_fee_rate = r.get_delivery_fee_rate()
        new_or_old.delivery_time = r.get_delivery_time()
        new_or_old.funding_interval = r.get_funding_interval()
        new_or_old.min_leverage = r.get_min_leverage()
        new_or_old.leverage_step = r.get_leverage_step()
        new_or_old.max_leverage = r.get_max_leverage()
        new_or_old.lower_funding_rate = r.get_lower_funding_rate()
        new_or_old.upper_funding_rate = r.get_upper_funding_rate()
        new_or_old.min_order_qty = r.get_min_order_qty()
        new_or_old.max_order_qty = r.get_max_order_qty()
        new_or_old.qty_step = r.get_qty_step()
        new_or_old.post_only_max_order_qty = r.get_post_only_max_order_qty()
        new_or_old.max_market_order_qty = r.get_max_market_order_qty()
        new_or_old.max_price = r.get_max_price()
        new_or_old.min_price = r.get_min_price()
        new_or_old.price_scale = r.get_price_scale()
        new_or_old.price_tick_size = r.get_price_tick_size()
        session.add(new_or_old)
        session.commit()


def process_spot_daily_data(session, ds):
    daily_tbl = Symbols.BBSpotSymbolsDaily
    ds_stmt = select(func.max(daily_tbl.downloaded_at).label("max_ds"))
    latest_ds = session.exec(ds_stmt).one_or_none()
    latest_snapshot = select(daily_tbl).where(daily_tbl.downloaded_at == latest_ds)
    ds_symbols = session.exec(latest_snapshot).all()

    for r in ds_symbols:
        stmt = select(Symbols.BBSpotSymbols)
        stmt = stmt.where(Symbols.BBSpotSymbols.symbol == r.symbol)
        new_or_old = session.exec(stmt).one_or_none()
        if new_or_old is None:
            new_or_old = Symbols.BBSpotSymbols(symbol=r.symbol)
        new_or_old.base_coin = r.get_base_coin()
        new_or_old.quote_coin = r.get_quote_coin()
        new_or_old.innovation = r.get_innovation()
        new_or_old.status = r.get_status()
        new_or_old.margin_trading = r.get_margin_trading()
        new_or_old.base_precision = r.get_base_precision()
        new_or_old.quote_precision = r.get_quote_precision()
        new_or_old.min_order_qty = r.get_min_order_qty()
        new_or_old.max_order_qty = r.get_max_order_qty()
        new_or_old.min_order_amt = r.get_min_order_amt()
        new_or_old.max_order_amt = r.get_max_order_amt()
        new_or_old.price_tick_size = r.get_price_tick_size()
        new_or_old.risk_limit_parameter = r.get_risk_limit_parameter()
        new_or_old.risk_market_parameter = r.get_risk_market_parameter()
        session.add(new_or_old)
        session.commit()


def get_logger(logger):
    handler = LogtailHandler(source_token=os.environ.get("LOGTAIL_SOURCE_TOKEN"))
    logger.setLevel(logging.INFO)
    logger.handlers = []
    logger.addHandler(handler)
    return logger

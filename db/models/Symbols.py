from datetime import date
from decimal import Decimal
from typing import Optional, Annotated
from click import Option
from sqlmodel import Field, SQLModel
from sqlalchemy import BigInteger, Column, DECIMAL


class BBPerpetualSymbolsDaily(SQLModel, table=True):
    __tablename__ = "bb_perp_symbols_daily"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    downloaded_at: date = date.today()
    symbol: str
    status: Optional[str]
    contract_type: Optional[str]
    copy_trading: Optional[str]
    has_unified_margin_trade: Optional[str]
    base_coin: Optional[str]
    quote_coin: Optional[str]
    settle_coin: Optional[str]
    launch_time: Optional[str]
    delivery_fee_rate: Optional[str]
    delivery_time: Optional[str]
    funding_interval: Optional[str]
    # leverage
    min_leverage: Optional[str]
    leverage_step: Optional[str]
    max_leverage: Optional[str]
    # funding rate
    lower_funding_rate: Optional[str]
    upper_funding_rate: Optional[str]
    # qty columns
    min_order_qty: Optional[str]
    max_order_qty: Optional[str]
    qty_step: Optional[str]
    post_only_max_order_qty: Optional[str]
    max_market_order_qty: Optional[str]
    # price columns
    max_price: Optional[str]
    min_price: Optional[str]
    price_scale: Optional[str]
    price_tick_size: Optional[str]

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
    status: str
    contract_type: str
    copy_trading: Optional[str]
    has_unified_margin_trade: bool
    base_coin: str
    quote_coin: str
    settle_coin: str
    launch_time: Optional[int] = Field(sa_column=Column(BigInteger()))
    delivery_fee_rate: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    delivery_time: Optional[int] = Field(sa_column=Column(BigInteger()))
    funding_interval: Optional[int] = Field(sa_column=Column(BigInteger()))
    # leverage
    min_leverage: Optional[Decimal] = Field(sa_column=DECIMAL(5, 2))
    leverage_step: Optional[Decimal] = Field(sa_column=DECIMAL(5, 2))
    max_leverage: Optional[Decimal] = Field(sa_column=DECIMAL(5, 2))
    # funding rate
    lower_funding_rate: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    upper_funding_rate: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    # qty columns
    min_order_qty: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    max_order_qty: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    qty_step: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    post_only_max_order_qty: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    max_market_order_qty: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    # price columns
    max_price: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    min_price: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))
    price_scale: Optional[int]
    price_tick_size: Optional[Decimal] = Field(sa_column=DECIMAL(38, 10))

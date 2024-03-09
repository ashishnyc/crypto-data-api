from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from sqlmodel import Field, SQLModel
from db.models import Constants
import utils


class BBPerpetualSymbolsDaily(SQLModel, table=True):
    __tablename__ = "bb_perp_symbols_daily"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    downloaded_at: str = "1900-01-01 00:00:00"
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

    def get_status(self) -> str:
        status = self.status or Constants.UNKNOWN
        status = utils.update_none_to_unknown(status)
        return status

    def get_contract_type(self) -> str:
        contract_type = self.contract_type or Constants.UNKNOWN
        contract_type = utils.update_none_to_unknown(contract_type)
        return contract_type

    def get_has_unified_margin_trade(self) -> str:
        unified_margin_trade = self.has_unified_margin_trade or Constants.UNKNOWN
        unified_margin_trade = utils.update_none_to_unknown(unified_margin_trade)
        return unified_margin_trade

    def get_base_coin(self) -> str:
        coin = self.base_coin or Constants.UNKNOWN
        coin = utils.update_none_to_unknown(coin)
        return coin

    def get_quote_coin(self) -> str:
        coin = self.quote_coin or Constants.UNKNOWN
        coin = utils.update_none_to_unknown(coin)
        return coin

    def get_settle_coin(self) -> str:
        coin = self.settle_coin or Constants.UNKNOWN
        coin = utils.update_none_to_unknown(coin)
        return coin

    def get_launch_time(self) -> datetime:
        launch_time = self.launch_time or "0"
        launch_time = launch_time.upper().replace("NONE", "0")
        return datetime.fromtimestamp(int(launch_time) / 1000.0)

    def get_delivery_fee_rate(self) -> Decimal:
        fee_rate = self.delivery_fee_rate or "0.0"
        fee_rate = fee_rate.upper().replace("NONE", "0.0")
        fee_rate = "0.0" if fee_rate == "" else fee_rate
        return Decimal(fee_rate)

    def get_delivery_time(self) -> datetime:
        delivery_time = self.delivery_time or "0"
        delivery_time = delivery_time.upper().replace("NONE", "0")
        return datetime.fromtimestamp(int(delivery_time) / 1000.0)

    def get_funding_interval(self) -> int:
        interval = self.funding_interval or "0"
        interval = interval.upper().replace("NONE", "0")
        return int(interval)

    def get_min_leverage(self) -> Decimal:
        leverage = self.min_leverage or "0.0"
        leverage = leverage.upper().replace("NONE", "0.0")
        return Decimal(leverage)

    def get_leverage_step(self) -> Decimal:
        step = self.leverage_step or "0.01"
        step = step.upper().replace("NONE", "0.01")
        return Decimal(step)

    def get_max_leverage(self) -> Decimal:
        leverage = self.max_leverage or "1.0"
        leverage = leverage.upper().replace("NONE", "1.0")
        return Decimal(leverage)

    def get_lower_funding_rate(self) -> Decimal:
        rate = self.lower_funding_rate or "0.0"
        rate = rate.upper().replace("NONE", "0.0")
        return Decimal(rate)

    def get_upper_funding_rate(self) -> Decimal:
        rate = self.upper_funding_rate or "0.0"
        rate = rate.upper().replace("NONE", "0.0")
        return Decimal(rate)

    def get_min_order_qty(self) -> Decimal:
        qty = self.min_order_qty or "0.00001"
        qty = qty.upper().replace("NONE", "0.00001")
        return Decimal(qty)

    def get_max_order_qty(self) -> Decimal:
        qty = self.max_order_qty or "0.00001"
        qty = qty.upper().replace("NONE", "0.00001")
        return Decimal(qty)

    def get_qty_step(self) -> Decimal:
        step = self.qty_step or "0.00001"
        step = step.upper().replace("NONE", "0.00001")
        return Decimal(step)

    def get_post_only_max_order_qty(self) -> Decimal:
        qty = self.post_only_max_order_qty or "0.0"
        qty = qty.upper().replace("NONE", "0.0")
        return Decimal(qty)

    def get_max_market_order_qty(self) -> Decimal:
        qty = self.max_market_order_qty or "0.0"
        qty = qty.upper().replace("NONE", "0.0")
        return Decimal(qty)

    def get_max_price(self) -> Decimal:
        price = self.max_price or "0.0"
        price = price.upper().replace("NONE", "0.0")
        return Decimal(price)

    def get_min_price(self) -> Decimal:
        price = self.min_price or "0.0"
        price = price.upper().replace("NONE", "0.0")
        return Decimal(price)

    def get_price_scale(self) -> int:
        scale = self.price_scale or "0"
        scale = scale.upper().replace("NONE", "0")
        return int(scale)

    def get_price_tick_size(self) -> Decimal:
        tick = self.price_tick_size or "0.0"
        tick = tick.upper().replace("NONE", "0.0")
        return Decimal(tick)


class BBPerpetualSymbols(SQLModel, table=True):
    __tablename__ = "bb_perp_symbols"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    status: Optional[str] = Constants.UNKNOWN
    contract_type: Optional[str] = Constants.UNKNOWN
    copy_trading: Optional[str] = Constants.UNKNOWN
    has_unified_margin_trade: Optional[str] = Constants.UNKNOWN
    base_coin: Optional[str] = Constants.UNKNOWN
    quote_coin: Optional[str] = Constants.UNKNOWN
    settle_coin: Optional[str] = Constants.UNKNOWN
    launch_time: datetime = Field(default_factory=datetime.now, nullable=False)
    delivery_fee_rate: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)

    delivery_time: datetime = Field(default_factory=datetime.now, nullable=True)
    funding_interval: Optional[int] = 8
    # leverage
    min_leverage: Decimal = Field(default=0.0, max_digits=10, decimal_places=2)
    leverage_step: Decimal = Field(default=0.01, max_digits=10, decimal_places=2)
    max_leverage: Decimal = Field(default=1.0, max_digits=10, decimal_places=2)
    # funding rate
    lower_funding_rate: Decimal = Field(default=0.0, max_digits=10, decimal_places=4)
    upper_funding_rate: Decimal = Field(default=0.0, max_digits=10, decimal_places=4)
    # qty columns
    min_order_qty: Decimal = Field(default=0.00001, max_digits=38, decimal_places=10)
    max_order_qty: Decimal = Field(default=0.00001, max_digits=38, decimal_places=10)
    qty_step: Decimal = Field(default=0.00001, max_digits=38, decimal_places=10)
    post_only_max_order_qty: Decimal = Field(
        default=0.0, max_digits=38, decimal_places=10
    )
    max_market_order_qty: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    # price columns
    max_price: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    min_price: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    price_scale: Optional[int] = 0
    price_tick_size: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)


class BBSpotSymbolsDaily(SQLModel, table=True):
    __tablename__ = "bb_spot_symbols_daily"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    downloaded_at: str = "1900-01-01 00:00:00"
    symbol: str
    base_coin: Optional[str]
    quote_coin: Optional[str]
    innovation: Optional[str]
    status: Optional[str]
    margin_trading: Optional[str]
    base_precision: Optional[str]
    quote_precision: Optional[str]
    min_order_qty: Optional[str]
    max_order_qty: Optional[str]
    min_order_amt: Optional[str]
    max_order_amt: Optional[str]
    price_tick_size: Optional[str]
    risk_limit_parameter: Optional[str]
    risk_market_parameter: Optional[str]

    def get_base_coin(self) -> str:
        coin = self.base_coin or Constants.UNKNOWN
        coin = utils.update_none_to_unknown(coin)
        return coin

    def get_quote_coin(self) -> str:
        coin = self.quote_coin or Constants.UNKNOWN
        coin = utils.update_none_to_unknown(coin)
        return coin

    def get_innovation(self) -> bool:

        innovation = self.innovation or "0"
        innovation = True if innovation == "1" else False
        return innovation

    def get_status(self) -> str:
        status = self.status or Constants.UNKNOWN
        status = utils.update_none_to_unknown(status)
        return status

    def get_margin_trading(self) -> str:
        margin = self.margin_trading or Constants.UNKNOWN
        margin = utils.update_none_to_unknown(margin)
        return margin

    def get_base_precision(self) -> Decimal:
        precision = self.base_precision or "0.0"
        precision = precision.upper().replace("NONE", "0.0")
        return Decimal(precision)

    def get_quote_precision(self) -> Decimal:
        precision = self.quote_precision or "0.0"
        precision = precision.upper().replace("NONE", "0.0")
        return Decimal(precision)

    def get_min_order_qty(self) -> Decimal:
        qty = self.min_order_qty or "0.0"
        qty = qty.upper().replace("NONE", "0.0")
        return Decimal(qty)

    def get_max_order_qty(self) -> Decimal:
        qty = self.max_order_qty or "0.0"
        qty = qty.upper().replace("NONE", "0.0")
        return Decimal(qty)

    def get_min_order_amt(self) -> Decimal:
        amt = self.min_order_amt or "0.0"
        amt = amt.upper().replace("NONE", "0.0")
        return Decimal(amt)

    def get_max_order_amt(self) -> Decimal:
        amt = self.max_order_amt or "0.0"
        amt = amt.upper().replace("NONE", "0.0")
        return Decimal(amt)

    def get_price_tick_size(self) -> Decimal:
        tick = self.price_tick_size or "0.0"
        tick = tick.upper().replace("NONE", "0.0")
        return Decimal(tick)

    def get_risk_limit_parameter(self) -> Decimal:
        risk = self.risk_limit_parameter or "0.0"
        risk = risk.upper().replace("NONE", "0.0")
        return Decimal(risk)

    def get_risk_market_parameter(self) -> Decimal:
        risk = self.risk_market_parameter or "0.0"
        risk = risk.upper().replace("NONE", "0.0")
        return Decimal(risk)


class BBSpotSymbols(SQLModel, table=True):
    __tablename__ = "bb_spot_symbols"  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    base_coin: Optional[str] = Constants.UNKNOWN
    quote_coin: Optional[str] = Constants.UNKNOWN
    innovation: Optional[bool] = Field(default=False)
    status: Optional[str] = Constants.UNKNOWN
    margin_trading: Optional[str] = Constants.UNKNOWN
    base_precision: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    quote_precision: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    min_order_qty: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    max_order_qty: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    min_order_amt: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    max_order_amt: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    price_tick_size: Decimal = Field(default=0.0, max_digits=38, decimal_places=10)
    risk_limit_parameter: Decimal = Field(default=0.0, max_digits=10, decimal_places=2)
    risk_market_parameter: Decimal = Field(default=0.0, max_digits=10, decimal_places=2)

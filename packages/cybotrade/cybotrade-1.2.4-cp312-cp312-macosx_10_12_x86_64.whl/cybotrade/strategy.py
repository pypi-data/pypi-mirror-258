import logging
import asyncio

from json import JSONDecodeError
from aiohttp import web
from typing import Any, List, Dict

from .models import Candle, FloatWithTime, OpenedTrade, OrderUpdate, RuntimeMode, Interval

class Strategy:
    """
    This class is a handler that will be used by the Runtime to handle events such as
    `on_candle_closed`, `on_execution_update`, etc. The is a base class and every new strategy
    should be inheriting this class and override the methods.
    """

    logger = logging
    LOG_FORMAT = (
        "%(levelname)s %(name)s %(asctime)-15s %(filename)s:%(lineno)d %(message)s"
    )
    async def set_param(self, identifier: str, value: Any):
        """
        Used to set up params for the strategy
        """
        logging.info(f"Setting {identifier} to {value}")

    def __init__(
            self,
            log_level: int = logging.INFO,
            handlers: List[logging.Handler] = [],
    ):
        """
        Set up the logger
        """
        if len(handlers) == 0:
            default_handler = logging.StreamHandler()
            default_handler.setFormatter(logging.Formatter(self.LOG_FORMAT))
            handlers.append(default_handler)

        logging.root.setLevel(log_level)
        for handler in handlers:
            logging.root.addHandler(handler)

    async def on_init(self, strategy):
        logging.info(f"[on_init] Strategy successfully started.")

    async def on_trade(self, strategy, trade: OpenedTrade):
        logging.info(f"[on_trade] Received opened trade: {trade.__repr__()}")

    async def on_market_update(self, strategy, equity: FloatWithTime, available_balance: FloatWithTime):
        logging.info(
            f"[on_market_update] Received market update: equity({equity.__repr__()}), available_balance({available_balance.__repr__()})")

    async def on_order_update(self, strategy, update: OrderUpdate):
        logging.info(f"[on_order_update] Received order update: {update.__repr__()}")

    async def on_active_order_interval(self, strategy, active_orders: List[str]):
        logging.info(f"[on_active_order_interval] Received active orders: {active_orders.__repr__()}")

    async def on_backtest_complete(self, strategy):
        logging.info(f"[on_backtest_complete] Backtest completed.")

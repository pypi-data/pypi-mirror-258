import asyncio
import logging
from typing import Optional

from data_connectors_exchanges_coinapi.client.shared_data_streamer import SharedDataStreamer
from data_connectors_exchanges_coinapi.core.utils.async_utils import safe_ensure_future
from data_connectors_exchanges_coinapi.core.utils.time_formatter import the_time_in_iso_now_is
from data_connectors_exchanges_coinapi.logger import KomoLogger


class TradingSymbolDataProcessor:
    _logger: Optional[KomoLogger] = None

    @classmethod
    def logger(cls) -> KomoLogger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    def log_with_clock(self, log_level: int, msg: str, **kwargs):
        self.logger().log(log_level, f"{self.name} {msg} [clock={str(the_time_in_iso_now_is())}]", **kwargs)

    def __init__(self, input_data_queue: asyncio.Queue, output_data_queue: asyncio.Queue):
        self._input: asyncio.Queue = input_data_queue
        self._output: asyncio.Queue = output_data_queue

        self._trading_symbol_data_dispatcher_task: Optional[asyncio.Task] = None

    @property
    def name(self):
        return "trading_symbol_data_dispatcher"

    def start(self):
        self.log_with_clock(log_level=logging.INFO,
                            msg=f"Starting trading symbol data dispatcher. ")
        self._trading_symbol_data_dispatcher_task = safe_ensure_future(self.trading_symbol_data_dispatcher_loop())

    def stop(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Stopping trading symbol data dispatcher. ")
        # Clean up execution task.
        if self._trading_symbol_data_dispatcher_task is not None:
            self._trading_symbol_data_dispatcher_task.cancel()
            self._trading_symbol_data_dispatcher_task = None

    def publish(self, record: dict):
        try:
            safe_ensure_future(SharedDataStreamer.get_instance().exchange_data_stream.put(record))
        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Data publishing failure. {e}")
            return None

    async def trading_symbol_data_dispatcher_loop(self):
        while True:
            message = await self._input.get()
            self.publish(record=message.copy())

            # Quality assurance queue
            safe_ensure_future(self._output.put(message))

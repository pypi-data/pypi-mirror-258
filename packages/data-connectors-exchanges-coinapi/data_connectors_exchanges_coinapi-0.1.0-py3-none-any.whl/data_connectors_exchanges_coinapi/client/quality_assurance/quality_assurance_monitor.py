import asyncio
import logging
from typing import Optional

import pendulum

from data_connectors_exchanges_coinapi.core.utils.async_utils import safe_ensure_future
from data_connectors_exchanges_coinapi.core.utils.time_formatter import the_time_in_iso_now_is
from data_connectors_exchanges_coinapi.logger import KomoLogger


class QualityAssuranceMonitor:
    _logger: Optional[KomoLogger] = None

    @classmethod
    def logger(cls) -> KomoLogger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    def log_with_clock(self, log_level: int, msg: str, **kwargs):
        self.logger().log(log_level, f"{self.name} {msg} [clock={str(the_time_in_iso_now_is())}]", **kwargs)

    def __init__(self, input_data_queue: asyncio.Queue):
        self._input: asyncio.Queue = input_data_queue
        self._quality_assurance_task: Optional[asyncio.Task] = None

    @property
    def name(self):
        return "quality_assurance_monitor"

    def start(self):
        self.log_with_clock(log_level=logging.INFO,
                            msg=f"Starting quality assurance monitor. ")
        self._quality_assurance_task = safe_ensure_future(self.quality_assurance_loop())

    def stop(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Stopping quality assurance monitor. ")
        # Clean up execution task.
        if self._quality_assurance_task is not None:
            self._quality_assurance_task.cancel()
            self._quality_assurance_task = None

    async def quality_assurance_loop(self):
        while True:
            message = await self._input.get()
            # print(message)
            exchange_dt: Optional[pendulum.Date] = None
            now: Optional[pendulum.Date] = None

            elapsed = exchange_dt.diff(now).in_seconds()

            if elapsed > 2:
                # LOG
                pass

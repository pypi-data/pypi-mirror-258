import asyncio
import logging
from typing import Optional

from data_connectors_exchanges_coinapi.core.utils.async_utils import safe_ensure_future
from data_connectors_exchanges_coinapi.core.utils.time_formatter import the_time_in_iso_now_is, \
    give_me_a_timestamp_from_this_string
from data_connectors_exchanges_coinapi.logger import KomoLogger


class ExchangeDataProcessor:
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

        self._exchange_data_processor_task: Optional[asyncio.Task] = None

    @property
    def name(self):
        return "exchange_data_processor"

    def start(self):
        # print("iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        self._exchange_data_processor_task = safe_ensure_future(self.exchange_data_processor_loop())

    def stop(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Stopping exchange data parsing and processing. ")
        # Clean up execution task.
        if self._exchange_data_processor_task is not None:
            self._exchange_data_processor_task.cancel()
            self._exchange_data_processor_task = None

    def parse(self, record: dict):
        try:
            if str(record['symbol_id']).upper().split('_')[1] not in ['SPOT']:
                # print(str(record['symbol_id']).lower().split('_')[1])
                return None

            return record
        except KeyError as ke:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Record processing failure. Key missing. {ke}")
            return None
        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Record processing failure. {e}")
            return None

    def process(self, record: dict):
        try:
            record['base'] = str(record['symbol_id']).upper().split('_')[2]
            record['quote'] = str(record['symbol_id']).upper().split('_')[3]
            record['exchange'] = str(record['symbol_id']).lower().split('_')[0]
            record['amount'] = record.pop('size')
            record['symbol'] = record.pop('symbol_id')
            record['side'] = record.pop('taker_side')
            record['timestamp_at_exchange'] = record['time_exchange']
            record['timestamp_at_exchange_float'] = give_me_a_timestamp_from_this_string(str_date=record['time_exchange'])
            record['timestamp_at_connector'] = the_time_in_iso_now_is()
            # print(record)
            return record
        except KeyError as ke:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Record processing failure. Key missing. {ke}")
            return None
        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Record processing failure. {e}")
            return None

    async def exchange_data_processor_loop(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Starting exchange data parsing and processing loop. ")
        while True:
            message = await self._input.get()
            # print(message)
            parsed = self.parse(record=message)
            if parsed is None:
                continue

            processed = self.process(record=parsed)
            if processed is None:
                continue

            safe_ensure_future(self._output.put(processed))

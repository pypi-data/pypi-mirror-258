import asyncio
import json
import logging
from statistics import mean
from typing import Optional, Dict

import numpy as np
import websockets
from cachetools import FIFOCache

from data_connectors_exchanges_coinapi.core.utils.async_utils import safe_ensure_future
from data_connectors_exchanges_coinapi.core.utils.time_formatter import the_time_in_iso_now_is
from data_connectors_exchanges_coinapi.logger import KomoLogger
from data_connectors_exchanges_coinapi.shared_setup import SharedSetup


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


class FallBackTSOPriceSignaler:
    _logger: Optional[KomoLogger] = None

    @classmethod
    def logger(cls) -> KomoLogger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    def log_with_clock(self, log_level: int, msg: str, **kwargs):
        self.logger().log(log_level, f"{self.__class__.__name__} {msg} [clock={str(the_time_in_iso_now_is())}]",
                          **kwargs)

    def __init__(self, input_data_queue: asyncio.Queue):
        self._input: asyncio.Queue = input_data_queue
        self._price_publication_loop_task: Optional[asyncio.Task] = None
        self._price_collection_loop_task: Optional[asyncio.Task] = None
        self.last_tso_prices: Dict[str, FIFOCache] = {}

    def start(self):
        safe_ensure_future(self.price_collection_loop())
        safe_ensure_future(self.price_publication_loop())

    async def publish(self, data: dict):
        for chain in ['flare', 'songbird']:
            publish_to_endpoint = f"ws://{SharedSetup.get_instance().chain_tso_ws_endpoints[chain]}"
            self.log_with_clock(log_level=logging.DEBUG, msg=f"Publishing price data. {publish_to_endpoint}")
            async with websockets.connect(publish_to_endpoint) as websocket:
                await websocket.send(json.dumps(data, cls=NpEncoder))

    async def price_publication_loop(self):
        while True:
            prices: dict = {}
            for tso, fc in self.last_tso_prices.items():
                prices[tso] = mean(list(fc.values()))

            data = {
                "algorithm": "coinapi_connector",
                "data": prices,
                "type": "fallback_prices",
                "time": the_time_in_iso_now_is()
            }
            # print(data)
            safe_ensure_future(self.publish(data=data))
            await asyncio.sleep(10)

    async def price_collection_loop(self):
        print("**********************************************")
        while True:
            message = await self._input.get()
            # print(message)
            tso = str(message['symbol']).split('_')[2]
            if tso not in self.last_tso_prices:
                self.last_tso_prices[tso] = FIFOCache(15)

            self.last_tso_prices[tso].update({message['uuid']: message['price']})

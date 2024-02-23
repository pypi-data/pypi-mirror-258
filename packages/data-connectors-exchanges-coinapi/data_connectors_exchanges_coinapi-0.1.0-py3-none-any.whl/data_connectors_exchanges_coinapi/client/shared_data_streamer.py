import asyncio
import json
import logging
from typing import Optional

# Server data
import websockets
from komoutils.core
from komoutils.core.time import the_time_in_iso_now_is
from komoutils.logger import KomoLogger

from data_connectors_exchanges_coinapi.shared_setup import SharedSetup


class SharedDataStreamer:
    _shared_instance: "SharedDataStreamer" = None
    _logger: Optional[KomoLogger] = None

    @classmethod
    def get_instance(cls) -> "SharedDataStreamer":
        if cls._shared_instance is None:
            cls._shared_instance = SharedDataStreamer()
        return cls._shared_instance

    @classmethod
    def logger(cls) -> KomoLogger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    def log_with_clock(self, log_level: int, msg: str, **kwargs):
        self.logger().log(log_level, f"{self.__class__.__name__} {msg} [clock={str(the_time_in_iso_now_is())}]",
                          **kwargs)

    def __init__(self):

        self._client: Optional[websockets.WebSocketClientProtocol] = None
        self._exchange_data_stream: asyncio.Queue = asyncio.Queue()
        self._exchange_data_stream_task: Optional[asyncio.Task] = None

    @property
    def name(self):
        return "shared_data_stream"

    @property
    def exchange_data_stream(self) -> asyncio.Queue:
        return self._exchange_data_stream

    def start(self):
        self._exchange_data_stream_task = safe_ensure_future(self._trades_data_stream_loop())

    async def _trades_data_stream_loop(self):
        self.log_with_clock(log_level=logging.INFO,
                            msg=f"Establishing a connection to {SharedSetup.get_instance().exchanges_data_streamer_endpoint}. ")
        try:
            async with websockets.connect(SharedSetup.get_instance().exchanges_data_streamer_endpoint) as websocket:
                self.log_with_clock(log_level=logging.INFO,
                                    msg=f"Connection to {SharedSetup.get_instance().exchanges_data_streamer_endpoint} "
                                        f"for {self.name} exchange data is now active. ")
                while True:
                    message = await self._exchange_data_stream.get()
                    message['time_dispatched_at_connector'] = the_time_in_iso_now_is()
                    data = {
                        'type': 'exchange_data_trades',
                        'exchange': message['exchange'],
                        'source': 'trades',
                        'data': message
                    }
                    await websocket.send(json.dumps(data))
                    # print(f"MESSSAGE SENT {data}")
                    self._exchange_data_stream.task_done()

        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Connection was closed. Will retry {e}")
            print(f"MESSSAGE SENT {data}")
            # await asyncio.sleep(1)
            safe_ensure_future(self._trades_data_stream_loop())
            raise

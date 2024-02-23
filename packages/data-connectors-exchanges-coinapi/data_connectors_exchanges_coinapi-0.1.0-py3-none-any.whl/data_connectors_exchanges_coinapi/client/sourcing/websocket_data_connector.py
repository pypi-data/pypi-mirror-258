import asyncio
import json
import logging
from typing import AsyncIterable, Optional

import websockets

from data_connectors_exchanges_coinapi import get_api_setup_data
from data_connectors_exchanges_coinapi.core.utils.async_utils import safe_ensure_future
from data_connectors_exchanges_coinapi.core.utils.time_formatter import the_time_in_iso_now_is
from data_connectors_exchanges_coinapi.logger import KomoLogger
from data_connectors_exchanges_coinapi.shared_setup import SharedSetup


class CoinAPIv1Subscribe(object):
    def __init__(self, symbols: list, api_key: str):
        self.type = "hello"
        self.apikey = api_key
        self.heartbeat = True
        self.subscribe_data_type = ["trade"]
        self.subscribe_filter_symbol_id = symbols


class WebsocketDataConnector:
    MESSAGE_TIMEOUT = 30.0
    RECONNECTION_INTERVAL = 3
    PING_TIMEOUT = 10.0

    _logger: Optional[KomoLogger] = None

    @classmethod
    def logger(cls) -> KomoLogger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    def log_with_clock(self, log_level: int, msg: str, **kwargs):
        self.logger().log(log_level, f"{self.name} {msg} [clock={str(the_time_in_iso_now_is())}]", **kwargs)

    def __init__(self, output: asyncio.Queue, symbols: list):
        self._output: asyncio.Queue = output

        self._setup = get_api_setup_data()
        self._coinapi_ws_url = SharedSetup.get_instance().coinapi_wss
        self._coinapi_key = SharedSetup.get_instance().coinapi_key

        self._subscribe_request: dict = CoinAPIv1Subscribe(symbols, self._coinapi_key).__dict__
        self._data_connection_task: Optional[asyncio.Task] = None
        self._symbols = symbols

    @property
    def name(self):
        return "websocket_data_connector"

    def start(self):
        self.log_with_clock(log_level=logging.INFO,
                            msg=f"Starting trades websocket connection. Listening for {len(self._symbols)} symbols. ")
        self._data_connection_task = safe_ensure_future(self.data_connection_loop())

    def stop(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Stopping trades websocket connection. ")
        # Clean up execution task.
        if self._data_connection_task is not None:
            self._data_connection_task.cancel()
            self._data_connection_task = None

    async def _inner_messages(self, ws: websockets.WebSocketClientProtocol) -> AsyncIterable[str]:
        """
        Generator function that returns messages from the web socket stream
        :param ws: current web socket connection
        :returns: message in AsyncIterable format
        """
        # Terminate the recv() loop as soon as the next message timed out, so the outer loop can reconnect.
        try:
            while True:
                try:
                    msg: str = await asyncio.wait_for(ws.recv(), timeout=self.MESSAGE_TIMEOUT)
                    yield msg
                except asyncio.TimeoutError:
                    try:
                        pong_waiter = await ws.ping()
                        await asyncio.wait_for(pong_waiter, timeout=self.PING_TIMEOUT)
                    except asyncio.TimeoutError:
                        raise
        except asyncio.TimeoutError:
            self.logger().warning("WebSocket ping timed out. Going to reconnect...")
            return
        except websockets.ConnectionClosed:
            return
        finally:
            await ws.close()

    async def data_connection_loop(self):

        self.log_with_clock(log_level=logging.INFO ,msg=f"Starting trade accumulation loop. {self._coinapi_ws_url}")
        while True:
            try:
                async with websockets.connect(self._coinapi_ws_url) as websocket:
                    ws: websockets.WebSocketClientProtocol = websocket
                    await ws.send(json.dumps(self._subscribe_request))
                    async for raw_msg in self._inner_messages(ws):
                        message = json.loads(raw_msg)

                        print(message)
                        msg_type: str = message.get("type", None)
                        if msg_type in ["trade"]:
                            self._output.put_nowait(message)
                            continue
                        if msg_type is None:
                            raise ValueError(f"Websocket message does not contain a type - {message}")
                        elif msg_type == "error":
                            raise ValueError(f"Websocket received error message - {message}")
                        elif msg_type in ["heartbeat", "hearbeat"]:
                            self.log_with_clock(log_level=logging.INFO, msg=f"Heartbeat message received at {the_time_in_iso_now_is()}")
                        else:
                            raise ValueError(f"Unrecognized CoinAPI Websocket message received - {message}")

            except asyncio.CancelledError as ve:
                self.log_with_clock(log_level=logging.ERROR, msg=f"CancelledError {ve}")
            except ConnectionRefusedError as ve:
                self.logger().error(f"Connection to {self._coinapi_ws_url} has been refused. Is the server running? "
                                    f"Will try again in {self.RECONNECTION_INTERVAL} second(s).")
                await asyncio.sleep(self.RECONNECTION_INTERVAL)

            except ValueError as ve:
                self.log_with_clock(log_level=logging.ERROR, msg=f"{ve}")
                await asyncio.sleep(3.0)

            except Exception as e:
                self.log_with_clock(log_level=logging.ERROR, msg=f"{e}")
                await asyncio.sleep(3.0)

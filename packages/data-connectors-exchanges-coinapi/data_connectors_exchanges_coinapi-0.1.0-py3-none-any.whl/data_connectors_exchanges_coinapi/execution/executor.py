import asyncio
import logging
from typing import Optional

from data_connectors_exchanges_coinapi.client.dispatching.fallback_tso_price_signaler import FallBackTSOPriceSignaler
from data_connectors_exchanges_coinapi.client.dispatching.trading_symbol_data_dispatcher import TradingSymbolDataProcessor
from data_connectors_exchanges_coinapi.client.processing.exchange_data_processor import ExchangeDataProcessor
from data_connectors_exchanges_coinapi.client.quality_assurance.quality_assurance_monitor import QualityAssuranceMonitor
from data_connectors_exchanges_coinapi.client.shared_data_streamer import SharedDataStreamer
from data_connectors_exchanges_coinapi.client.sourcing.websocket_data_connector import WebsocketDataConnector
from data_connectors_exchanges_coinapi.core.utils.time_formatter import the_time_in_iso_now_is
from data_connectors_exchanges_coinapi.db.crud import read_symbol_metadata
from data_connectors_exchanges_coinapi.logger import KomoLogger
from data_connectors_exchanges_coinapi.shared_setup import SharedSetup


class Executor:
    _tso_pas_logger: Optional[KomoLogger] = None

    @classmethod
    def logger(cls) -> KomoLogger:
        if cls._tso_pas_logger is None:
            cls._tso_pas_logger = logging.getLogger(__name__)
        return cls._tso_pas_logger

    def log_with_clock(self, log_level: int, msg: str, **kwargs):
        self.logger().log(log_level, f"{msg} [clock={str(the_time_in_iso_now_is())}]", **kwargs)

    def __init__(self):
        super().__init__()
        self._processing_queue: asyncio.Queue = asyncio.Queue()
        self._dispatching_queue: asyncio.Queue = asyncio.Queue()
        self._quality_assurance_queue: asyncio.Queue = asyncio.Queue()
        self._tso_fallback_queue: asyncio.Queue = asyncio.Queue()

        self.connector: Optional[WebsocketDataConnector] = None
        self.processor: Optional[ExchangeDataProcessor] = None
        self.dispatcher: Optional[TradingSymbolDataProcessor] = None
        self.monitor: Optional[QualityAssuranceMonitor] = None
        self.tso_fallback: Optional[FallBackTSOPriceSignaler] = None

        self.symbols: list = []

    @property
    def name(self):
        return "executor"

    def load_symbols(self):
        # assets = SharedSetup.get_instance().a
        self.symbols = [s['symbol'] for s in read_symbol_metadata()]

    def initialize(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Starting executor initialization. {len(self.symbols)} will "
                                                        f"be processed. ")
        SharedSetup.get_instance().start()

        self.connector = WebsocketDataConnector(output=self._processing_queue, symbols=self.symbols)
        self.processor = ExchangeDataProcessor(input_data_queue=self._processing_queue,
                                               output_data_queue=self._dispatching_queue)
        self.dispatcher = TradingSymbolDataProcessor(input_data_queue=self._dispatching_queue,
                                                     output_data_queue=self._tso_fallback_queue)
        # self.monitor = QualityAssuranceMonitor(input_data_queue=self._quality_assurance_queue)
        self.tso_fallback = FallBackTSOPriceSignaler(input_data_queue=self._tso_fallback_queue)

    def start(self):
        self.load_symbols()
        self.initialize()
        SharedDataStreamer.get_instance().start()
        self.tso_fallback.start()
        # self.monitor.start()
        self.dispatcher.start()
        self.processor.start()
        self.connector.start()

    def stop(self):
        pass

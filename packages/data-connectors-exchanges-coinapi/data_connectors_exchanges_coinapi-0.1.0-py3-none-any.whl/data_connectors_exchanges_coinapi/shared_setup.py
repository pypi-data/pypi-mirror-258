import logging
import os
from os.path import basename, dirname, abspath
from typing import Optional

from komoutils.core.time import the_time_in_iso_now_is
from komoutils.logger import KomoLogger

from data_connectors_exchanges_coinapi import get_api_setup_data


class SharedSetup:
    _shared_instance: "SharedSetup" = None
    _logger: Optional[KomoLogger] = None

    @classmethod
    def get_instance(cls) -> "SharedSetup":
        if cls._shared_instance is None:
            cls._shared_instance = SharedSetup()
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
        self.setup_data = get_api_setup_data()
        self.algorithm_name: str = ""
        self.symbols: list = []

        self.chain_tso_ws_endpoints: dict = {}
        self.exchanges_data_streamer_endpoint: str = ''
        self.mongo_uri = self.setup_data["environments"]["databases"]["mongo"]["uri"]
        self.db: str = 'combined'

        self.coinapi_url: str = self.setup_data["third-party-services"]["coinapi"]["url"]
        self.coinapi_wss: str = self.setup_data["third-party-services"]["coinapi"]["wss"]
        self.coinapi_key: str = self.setup_data["third-party-services"]["coinapi"]["key"]

        self.exchanges: list = []
        self.assets: list = []
        self.quotes: list = []

    def start(self):
        self.log_with_clock(log_level=logging.INFO, msg=f"Shared algorithm setup service started. ")

        try:
            # Get the name of the algorithm for dir name
            self.algorithm_name = str(basename(dirname(abspath(__file__)))).replace("_", "-")
            print(f"Service name {self.algorithm_name}")
            # Check if the algo is configured on the Setup URL.
            # if self.algorithm_name not in self.setup_data["ml"]:
            #     raise Exception(f"{self.algorithm_name} is not registered on TSO setup. ")
            self.chain_tso_ws_endpoints: dict = self.setup_data['tso']['services']['chains']
            self.exchanges_data_streamer_endpoint = f"ws://{self.setup_data['exchanges']['services']['data']['url']}"

            self.exchanges: list = self.setup_data['exchanges']['venues']
            self.quotes: list = self.setup_data['exchanges']['tracked_assets']
            self.quotes: list = self.setup_data['exchanges']['tracked_quotes']



        except Exception as e:
            raise e

        self.log_with_clock(log_level=logging.INFO, msg=f"Shared algorithm setup service successfully started. ")

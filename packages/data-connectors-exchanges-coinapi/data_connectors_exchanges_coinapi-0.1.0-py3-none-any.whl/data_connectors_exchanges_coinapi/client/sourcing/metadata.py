import logging
import random
from typing import Optional

import requests

from data_connectors_exchanges_coinapi.core.utils.time_formatter import the_time_in_iso_now_is
from data_connectors_exchanges_coinapi.db.crud import write_symbol_metadata
from data_connectors_exchanges_coinapi.db.mongodb_reader_writer import MongoDBReaderWriter
from data_connectors_exchanges_coinapi.logger import KomoLogger
from data_connectors_exchanges_coinapi.shared_setup import SharedSetup


class Metadata:
    _logger: Optional[KomoLogger] = None

    @classmethod
    def logger(cls) -> KomoLogger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    def log_with_clock(self, log_level: int, msg: str, **kwargs):
        self.logger().log(log_level, f"{self.name} {msg} [clock={str(the_time_in_iso_now_is())}]", **kwargs)

    def __init__(self):
        self.url = SharedSetup.get_instance().coinapi_url
        # self.key = '284269B4-BCEA-4764-AA35-69333D5A88B2'
        self.key = SharedSetup.get_instance().coinapi_key

        self.errors: list = []
        self.existing: list= []

    @property
    def name(self):
        return "metadata"

    def symbol_id_generator(self):
        while True:
            _id: int = random.randint(10000, 99999)
            if _id in self.existing:
                continue
            else:
                self.existing.append(_id)
                return _id

    def get_symbols_data_by_exchange(self, exchange_id: str):
        try:
            self.log_with_clock(log_level=logging.INFO, msg=f"Sourcing records for {exchange_id}. ")
            payload = {}
            headers = {
                'Accept': 'application/json',
                'X-CoinAPI-Key': self.key
            }

            response = requests.request("GET", f'{self.url}/symbols/{exchange_id}', headers=headers, data=payload)
            print(response)
            data: list = []
            for result in response.json():
                if 'asset_id_base' not in result:
                    continue
                if 'asset_id_quote' not in result:
                    continue

                if (result['asset_id_base'] in SharedSetup.get_instance().assets
                        and result['asset_id_quote'] in SharedSetup.get_instance().quotes):
                    data.append({
                        'symbol_number': self.symbol_id_generator(),
                        'symbol': result['symbol_id'],
                        'exchange': result['exchange_id'],
                        'base': result['asset_id_base'],
                        'quote': result['asset_id_quote'],
                    })

            self.log_with_clock(log_level=logging.INFO, msg=f"Found {len(data)} symbol records for {exchange_id}. ")
            return data
        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"{exchange_id} {e}. ")
            self.errors.append(exchange_id)
            # raise

    def get_symbols_data(self):
        symbol_records: list = []
        for exchange in sorted(SharedSetup.get_instance().exchanges):
            r = self.get_symbols_data_by_exchange(exchange_id=exchange)
            symbol_records.extend(r)

        write_symbol_metadata(data=symbol_records)
        return symbol_records

    def get_exchange_data(self):

        try:
            payload = {}
            headers = {
                'Accept': 'application/json',
                'X-CoinAPI-Key': self.key
            }

            response = requests.request("GET", f'{self.url}/exchanges', headers=headers, data=payload)
            exchange_name_id_pair = {exchange['exchange_id']: exchange['name'] for exchange in response.json() if
                                     'name' in exchange}
            print(sorted(exchange_name_id_pair.keys()))
        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"{e}")
            raise

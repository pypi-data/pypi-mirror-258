import logging
from typing import Optional, Any, Union

import pymongo
from pymongo.cursor import Cursor

from komoutils.core.time import the_time_in_iso_now_is
from komoutils.logger import KomoLogger


class MongoDBReaderWriter:
    _logger: Optional[KomoLogger] = None

    @classmethod
    def logger(cls) -> KomoLogger:
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
        return cls._logger

    def log_with_clock(self, log_level: int, msg: str, **kwargs):
        self.logger().log(log_level, f"{self.__class__.__name__} {msg} [clock={str(the_time_in_iso_now_is())}]",
                          **kwargs)

    def __init__(self, uri: str, db_name: str, collection: str):
        self.client: pymongo.MongoClient = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection: str = collection

    @property
    def name(self):
        return "mongodb_reader_writer"

    def start(self):
        pass

    def read_symbol_list_by_tso(self, filters: dict):
        symbols: list = self.db[self.collection].find(filters).distinct("symbol")
        return symbols

    def read_latest_result_by_tso(self, filters: dict, limit: int = 1):

        results: Cursor = self.db[self.collection].find(filters).sort('epoch', -1).limit(limit)
        data = list(results)

        assert len(data) > 0, f"Cursor has no records. "

        return data[0]

    def read_latest_trade_by_symbol(self, filters: dict, limit: int = 1):
        try:
            results: Cursor = self.db[self.collection].find(filters).sort('timestamp_at_exchange', -1).limit(limit)

            data = list(results)

            assert len(data) > 0, f"Symbol has no records. "

            return data[0]
        except AssertionError as ae:
            raise ae

        except Exception as e:
            raise e

    def read(self, filters: dict, omit: dict, limit: int = 1000000):
        records: list = list(self.db[self.collection].find(filters, omit).sort('_id', -1).limit(limit=limit))
        return records

    def write(self, data: Union[list, dict]):
        if len(data) == 0:
            self.log_with_clock(log_level=logging.INFO,
                                msg=f"0 records to send for collection {self.collection}. ")
            return
        # print(f"++++++++++++++++++++++++++++++++++++++++++++++++")
        try:
            if isinstance(data, dict):
                self.db[self.collection].insert_one(data)
            elif isinstance(data, list):
                self.db[self.collection].insert_many(data)

            self.log_with_clock(log_level=logging.DEBUG, msg=f"Successfully sent {self.collection} with size "
                                                             f"{len(data)} data to database. ")
            return 'success'
        except Exception as e:
            self.log_with_clock(log_level=logging.ERROR, msg=f"Unspecified error occurred. {e}")

    def updater(self, filters: dict, updater: dict):
        if len(updater) == 0:
            self.log_with_clock(log_level=logging.INFO,
                                msg=f"0 records to send for {self.db.upper()} for collection {self.collection}. ")
            return

        result = self.db[self.collection].update_one(filter=filters, update=updater, upsert=True)
        return result

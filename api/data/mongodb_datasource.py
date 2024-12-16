# File: db/mongodb_connection.py
from pymongo import MongoClient
from threading import Lock

class MongoDBConnection:
    _instance = None
    _lock = Lock()

    def __new__(cls, uri, database_name):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._client = MongoClient(uri)
                    cls._instance._db = cls._instance._client[database_name]
        return cls._instance

    def get_database(self):
        return self._db
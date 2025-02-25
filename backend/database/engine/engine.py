from ..connection import PostgresConnection
from .session import Session
from psycopg2.extensions import cursor as psycopg2_cursor
import psycopg2

from enum import Enum

from typing import Dict

class DatabaseEngine:
    def __init__(self, config: Dict[str, str] | None = None, url: str | None = None, autocommit: bool = False, log: bool = False):
        self.connection: PostgresConnection = PostgresConnection(config=config, url=url, autocommit=autocommit)
        self.log = log
        self._active = True

    def get_connection(self) -> PostgresConnection:
        return self.connection
    
    def cursor(self) -> psycopg2_cursor:
        return self.connection.cursor()

    def __enter__(self) -> 'DatabaseEngine':
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def session(self):
        return Session(self.connection, log=self.log)

    def close(self):
        if self._active:
            self._active = False
            self.connection.close_connection()

    def __destroy__(self):
        self.close()

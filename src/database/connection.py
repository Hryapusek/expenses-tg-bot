import psycopg2
from singleton_decorator import singleton
from configreader import ConfigReader
import threading
import logging

class DatabaseConnection:
    """
    Usage
    -----
    DatabaseConnection.connection()
    """
    connection_lock = threading.RLock()

    @staticmethod
    def connection():
        connection = psycopg2.connect(
            dbname = ConfigReader().db_name,
            user = ConfigReader().db_user,
            password = ConfigReader().db_password,
            host = ConfigReader().db_host,
            port = ConfigReader().db_port
        )
        connection.autocommit = True
        return connection

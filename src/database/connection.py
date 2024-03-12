import psycopg2
from singleton_decorator import singleton
from configreader import ConfigReader
import threading

class DatabaseConnection:
    """
    Usage
    -----
    DatabaseConnection.connection()
    """
    connection_lock = threading.RLock()

    @staticmethod
    def connection():
        if not 'connection_obj' in DatabaseConnection.__dict__:
            with DatabaseConnection.connection_lock:
                if not 'connection_obj' in DatabaseConnection.__dict__:
                    DatabaseConnection.reset_connection()
        return DatabaseConnection.connection_obj

    @staticmethod
    def reset_connection():
        DatabaseConnection.connection_obj = psycopg2.connect(
            dbname = ConfigReader().db_name,
            user = ConfigReader().db_user,
            password = ConfigReader().db_password,
            host = ConfigReader().db_host
        )

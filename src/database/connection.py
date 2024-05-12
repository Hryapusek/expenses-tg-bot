import psycopg2
from singleton_decorator import singleton
from configreader import ConfigReader
import logging

class DatabaseConnection:
    """
    Usage
    -----
    DatabaseConnection.connection()
    """
    @staticmethod
    def connection():
        connection = psycopg2.connect(
            dbname = ConfigReader().db_name,
            user = ConfigReader().db_user,
            password = ConfigReader().db_password,
            host = ConfigReader().db_host,
            port = ConfigReader().db_port
        )
        return connection

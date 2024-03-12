import psycopg2
from singleton_decorator import singleton
from configreader import ConfigReader

class DatabaseConnection:
    @staticmethod
    def connection():
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

from singleton_decorator import singleton
from .connection import DatabaseConnection
from .types.person import Person
import psycopg2


@singleton
class DatabaseApi:
    def get_person_by_id(id):
        """
        Returns
        -------
            Person: person object from table

        Raise
        -----
            - ProgrammingError if no person found
            - OperationalError if connection establishing failed
        """
        conn = DatabaseConnection.connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM person WHERE id = %s' % id)
            return Person.fromTuple(cursor.fetchone())

    def add_person(person):
        pass
    
    def add_cathegory(cathegory):
        pass

    def remove_cathegory(cathegory):
        pass
    
    def add_operation(operation):
        pass
    

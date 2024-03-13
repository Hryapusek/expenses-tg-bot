from singleton_decorator import singleton
from .connection import DatabaseConnection
from .types.person import Person
from .types.cathegory import Cathegory
import psycopg2


@singleton
class DatabaseApi:
    def get_person_by_id(self, id):
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

    def add_person(self, person: Person):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error error while inserting person
        """
        conn = DatabaseConnection.connection()
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO person(id, name, cathegory_ids, balance) VALUES (%s, \'%s\', ARRAY %s::integer[], %s)' % 
                           (person.id, person.name, person.cathegory_ids, person.balance))
    
    def __get_cathegory_type_id(self, cathegory_type: str):
        conn = DatabaseConnection.connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id FROM cathegory_type WHERE type_name = \'%s\'' % (cathegory_type))
            return cursor.fetchone()[0]
        
    def __get_operation_type_id(self, operation_type: str):
        conn = DatabaseConnection.connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT id FROM operation_type WHERE type_name = \'%s\'' % (operation_type))
            return cursor.fetchone()[0]

    def get_income_cathegory_type_id(self):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        return self.__get_cathegory_type_id('income')

    def get_expense_cathegory_type_id(self):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        return self.__get_cathegory_type_id('expense')
    
    def get_income_operation_type_id(self):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        return self.__get_operation_type_id('income')

    def get_expense_operation_type_id(self):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        return self.__get_operation_type_id('expense')

    def add_cathegory(self, cathegory: Cathegory) -> int:
        """
        Returns
        -------
        id of inserted row

        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        conn = DatabaseConnection.connection()
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO cathegory(person_id, cathegory_type_id, name, money_limit, current_money '
                           'VALUES(%s, %s, \'%s\', %s, %s) RETURNING id' % (cathegory.person_id, cathegory.cathegory_type_id, 
                                                                        cathegory.name, cathegory.money_limit, cathegory.current_money))
            return cursor.fetchone()[0]

    def remove_cathegory(self, cathegory):
        pass
    
    def add_operation(self, operation):
        pass

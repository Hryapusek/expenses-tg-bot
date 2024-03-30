from singleton_decorator import singleton
from .connection import DatabaseConnection
from .types.person import Person
from .types.cathegory import Cathegory
from .types.operation import Operation
from functools import lru_cache
import psycopg2
import logging


@singleton
class DatabaseApi:
    def get_person_by_id(self, person_id):
        """
        Raise
        -----
            - ProgrammingError if no person found
            - OperationalError if connection establishing failed
        """
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM person WHERE id = %s", (person_id,))
                result = cursor.fetchone()
                if result is None:
                    raise psycopg2.ProgrammingError(
                        "Person with id %s was not found" % (person_id,)
                    )
        finally:
            conn.commit()
            conn.close()
        return Person.fromTuple(result)

    def add_person(self, person: Person):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error error while inserting person
        """
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO person(id, name, cathegory_ids, balance) VALUES (%s, %s, %s, %s)",
                    (person.id, person.name, person.cathegory_ids, person.balance),
                )
        finally:
            conn.commit()
            conn.close()

    def remove_person_by_id(self, person_id):
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM person WHERE id = %s", (person_id,))
        finally:
            conn.commit()
            conn.close()

    def get_income_cathegory_type_id(self):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        return self.__get_cathegory_type_id("income")

    def get_expense_cathegory_type_id(self):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        return self.__get_cathegory_type_id("expense")

    def get_income_operation_type_id(self):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        return self.__get_operation_type_id("income")

    def get_expense_operation_type_id(self):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        return self.__get_operation_type_id("expense")

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
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO cathegory(person_id, cathegory_type_id, name, money_limit, current_money) "
                    "VALUES(%s, %s, %s, %s, %s) RETURNING id",
                    (
                        cathegory.person_id,
                        cathegory.cathegory_type_id,
                        cathegory.name,
                        cathegory.money_limit,
                        cathegory.current_money,
                    ),
                )
                inserted_cathegory_id = cursor.fetchone()[0]
                cursor.execute(
                    "UPDATE person SET cathegory_ids = ARRAY_APPEND(cathegory_ids, %s) WHERE id = %s",
                    (inserted_cathegory_id, cathegory.person_id),
                )
        finally:
            conn.commit()
            conn.close()
        return inserted_cathegory_id

    def get_cathegory_by_id(self, cathegory_id: int):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - ProgrammingError if no rows were found
            - psycopg2.Error for all other errors
        """
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cathegory WHERE id = %s", (cathegory_id,))
                result = cursor.fetchone()
                if result is None:
                    raise psycopg2.ProgrammingError(
                        "Cathergory with id %s was not found" % (cathegory_id,)
                    )
        finally:
            conn.commit()
            conn.close()
        return Cathegory.fromTuple(result)

    def add_operation(self, operation: Operation):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO operation(date, operation_type_id, person_id, cathegory_id, money_amount, commentary) "
                    "VALUES(%s, %s, %s, %s, %s, %s) RETURNING id",
                    (
                        operation.date,
                        operation.operation_type_id,
                        operation.person_id,
                        operation.cathegory_id,
                        operation.money_amout,
                        operation.comment,
                    ),
                )
                operation_id = cursor.fetchone()[0]
                # TODO: Add checking if cathegory_type has same type as operation_type
                # e.g. cathegory 'income' and operation 'income'
                # not the 'income' and 'expense'
                # Maybe this checking is too much need to think about it
                if operation.operation_type_id == self.get_income_operation_type_id():
                    cursor.execute(
                        "UPDATE cathegory SET current_money = current_money + %s "
                        "WHERE id = %s",
                        (operation.money_amout, operation.cathegory_id),
                    )
                    cursor.execute(
                        "UPDATE person SET balance = balance + %s " "WHERE id = %s",
                        (operation.money_amout, operation.person_id),
                    )

                elif operation.operation_type_id == self.get_expense_operation_type_id():
                    cursor.execute(
                        "UPDATE cathegory SET current_money = current_money - %s "
                        "WHERE id = %s",
                        (operation.money_amout, operation.cathegory_id),
                    )
                    cursor.execute(
                        "UPDATE person SET balance = balance - %s " "WHERE id = %s",
                        (operation.money_amout, operation.person_id),
                    )

                else:
                    logging.warning(
                        "Unknown operation type found in add_operation! Type id: %s",
                        operation.operation_type_id,
                    )
        finally:
            conn.commit()
            conn.close()
        return operation_id

    def truncate_table(self, table_name):
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('TRUNCATE TABLE "%s" CASCADE' % (table_name,))
        finally:
            conn.commit()
            conn.close()

    def remove_cathegory_by_id(self, cathegory_id):
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM cathegory WHERE id = %s RETURNING person_id",
                    (cathegory_id,),
                )
                person_id = cursor.fetchone()[0]
                cursor.execute(
                    "UPDATE person SET cathegory_ids = "
                    "ARRAY_REMOVE(cathegory_ids, %s) "
                    "WHERE id = %s",
                    (cathegory_id, person_id),
                )
        finally:
            conn.commit()
            conn.close()

    def get_person_all_cathegories_by_id(self, person_id: int):
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cathegory WHERE person_id = %s", (person_id,))
                result = [Cathegory.fromTuple(x) for x in cursor.fetchall()]
        finally:
            conn.commit()
            conn.close()
        return result
        
    def get_person_all_operations_by_ids(self, person_id: int, cathegory_id: int):
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM operation WHERE person_id = %s AND cathegory_id = %s", (person_id, cathegory_id))
                result = [Operation.fromTuple(x) for x in cursor.fetchall()]
        finally:
            conn.commit()
            conn.close()
        return result

    @lru_cache
    def __get_cathegory_type_id(self, cathegory_type: str):
        try:
            conn = DatabaseConnection.connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM cathegory_type WHERE type_name = %s",
                    (cathegory_type,),
                )
                result = cursor.fetchone()[0]
                if result is None:
                    raise psycopg2.ProgrammingError(
                        'Cathegory type "%s" was not found' % (cathegory_type,)
                    )
        finally:
            conn.commit()
            conn.close()
        return result

    @lru_cache
    def __get_operation_type_id(self, operation_type: str):
        conn = DatabaseConnection.connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM operation_type WHERE type_name = %s",
                    (operation_type,),
                )
                result = cursor.fetchone()[0]
                if result is None:
                    raise psycopg2.ProgrammingError(
                        'Operation type "%s" was not found' % (operation_type,)
                    )
        finally:
            conn.commit()
            conn.close()
        return result

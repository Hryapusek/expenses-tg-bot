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
    def get_person_by_id(self, person_id, conn = None):
        """
        Raise
        -----
            - ProgrammingError if no person found
            - OperationalError if connection establishing failed
        """
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM person WHERE id = %s", (person_id,))
                result = cursor.fetchone()
                if result is None:
                    raise psycopg2.ProgrammingError(
                        "Person with id %s was not found" % (person_id,)
                    )
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()
        return Person.fromTuple(result)

    def add_person(self, person: Person, conn = None):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error error while inserting person
        """
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO person(id, name, cathegory_ids, balance) VALUES (%s, %s, %s, %s)",
                    (person.id, person.name, person.cathegory_ids, person.balance),
                )
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()

    def remove_person_by_id(self, person_id, conn = None):
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM person WHERE id = %s", (person_id,))
        finally:
            if need_to_commit:
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

    def get_change_balance_operation_type_id(self):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        return self.__get_operation_type_id("change_balance")

    def add_cathegory(self, cathegory: Cathegory, conn = None) -> int:
        """
        Returns
        -------
        id of inserted row

        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
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
            if need_to_commit:
                conn.commit()
                conn.close()
        return inserted_cathegory_id

    def update_person(self, person: Person, conn = None):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE person SET name = %s, cathegory_ids = %s, balance = %s WHERE id = %s",
                    (person.name, person.cathegory_ids, person.balance, person.id),
                )
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()

    def update_cathegory(self, cathegory: Cathegory, conn = None):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE cathegory "
                    "SET cathegory_type_id = %s, "
                    "name = %s, "
                    "money_limit = %s, "
                    "current_money = %s "
                    "WHERE person_id = %s",
                    (
                        cathegory.cathegory_type_id,
                        cathegory.name,
                        cathegory.money_limit,
                        cathegory.current_money,
                        cathegory.person_id,
                    ),
                )
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()

    def get_cathegory_by_id(self, cathegory_id: int, conn = None):
        """
        Raise
        -----
            - OperationalError if connection establishing failed
            - ProgrammingError if no rows were found
            - psycopg2.Error for all other errors
        """
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cathegory WHERE id = %s", (cathegory_id,))
                result = cursor.fetchone()
                if result is None:
                    raise psycopg2.ProgrammingError(
                        "Cathergory with id %s was not found" % (cathegory_id,)
                    )
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()
        return Cathegory.fromTuple(result)

    def add_operation(self, operation: Operation, conn = None):
        """
        Returns
        -------
        id of inserted row

        Raise
        -----
            - OperationalError if connection establishing failed
            - psycopg2.Error for all other errors
        """
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
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
                        operation.money_amount,
                        operation.comment,
                    ),
                )
                operation_id = cursor.fetchone()[0]
                if operation.operation_type_id == self.get_change_balance_operation_type_id():
                    cursor.execute(
                        "UPDATE cathegory SET current_money = current_money + %s "
                        "WHERE id = %s",
                        (operation.money_amount, operation.cathegory_id),
                    )
                    cathegory = self.get_cathegory_by_id(operation.cathegory_id, conn)
                    if cathegory.cathegory_type_id == self.get_income_cathegory_type_id():
                        cursor.execute(
                            "UPDATE person SET balance = balance + %s " "WHERE id = %s",
                            (operation.money_amount, operation.person_id),
                        )
                    elif cathegory.cathegory_type_id == self.get_expense_cathegory_type_id():
                        cursor.execute(
                            "UPDATE person SET balance = balance - %s " "WHERE id = %s",
                            (operation.money_amount, operation.person_id),
                        )

                    else:
                        assert False, "Unknown operation type found in add_operation!"
                else:
                    assert False, "Unknown operation type found in add_operation!"
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()
        return operation_id

    def truncate_table(self, table_name, conn = None):
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute('TRUNCATE TABLE "%s" CASCADE' % (table_name,))
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()

    def remove_cathegory_by_id(self, cathegory_id, conn = None):
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
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
            if need_to_commit:
                conn.commit()
                conn.close()

    def get_person_all_cathegories_by_id(self, person_id: int, conn = None) -> list[Cathegory]:
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cathegory WHERE person_id = %s", (person_id,))
                result = [Cathegory.fromTuple(x) for x in cursor.fetchall()]
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()
        return result
        
    def get_person_all_operations_by_ids(self, person_id: int, cathegory_id: int, conn = None) -> list[Operation]:
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM operation WHERE person_id = %s AND cathegory_id = %s", (person_id, cathegory_id))
                result = [Operation.fromTuple(x) for x in cursor.fetchall()]
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()
        return result
    
    def get_operation_by_id(self, operation_id: int, conn = None):
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM operation WHERE id = %s", (operation_id,))
                result = cursor.fetchone()
                if result is None:
                    raise psycopg2.ProgrammingError(
                        "Operation with id %s was not found" % (operation_id,)
                    )
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()
        return Operation.fromTuple(result)

    def delete_operation_by_id(self, operation_id: int, conn = None):
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM operation WHERE id = %s", (operation_id,))
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()

    def rollback_operation(self, operation_id: int, conn = None):
        need_to_commit = False
        if conn is None:
            conn = DatabaseConnection.connection()
            need_to_commit = True
        try:
            operation: Operation = self.get_operation_by_id(operation_id, conn)
            cathegory: Cathegory = self.get_cathegory_by_id(operation.cathegory_id, conn)
            person: Person = self.get_person_by_id(operation.person_id, conn)
            if cathegory.cathegory_type_id == self.get_income_cathegory_type_id():
                cathegory.current_money -= operation.money_amount
                person.balance -= operation.money_amount
            elif cathegory.cathegory_type_id == self.get_expense_cathegory_type_id():
                cathegory.current_money += operation.money_amount
                person.balance += operation.money_amount
            self.delete_operation_by_id(operation_id, conn)
            self.update_cathegory(cathegory, conn)
            self.update_person(person, conn)
        finally:
            if need_to_commit:
                conn.commit()
                conn.close()

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

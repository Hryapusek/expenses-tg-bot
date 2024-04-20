import unittest
import psycopg2
from ..database_api import DatabaseApi
from ..types.person import Person 
from ..types.cathegory import Cathegory
from ..types.operation import Operation

class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        import logging_setup
        logging_setup.logging_setup()

    def test_simple_insert_person_1(self):
        self.__truncate_tables()
        person1 = Person(0, 'Amogus', [], 0)
        DatabaseApi().add_person(person1)

    def test_simple_insert_select_person_1(self):
        self.__truncate_tables()
        person1 = Person(0, 'Amogus', [], 0)
        DatabaseApi().add_person(person1)
        fetched_person = DatabaseApi().get_person_by_id(0)
        self.assertEqual(person1, fetched_person)

    def test_simple_insert_select_remove_cathegory_1(self):
        self.__truncate_tables()
        person1 = Person(0, 'Amogus', [], 0)
        DatabaseApi().add_person(person1)
        cathegory = Cathegory(0, 0, DatabaseApi().get_expense_cathegory_type_id(),
                              'example_cathegory_1', 1000, 0)
        
        cathegory.id = DatabaseApi().add_cathegory(cathegory)
        fetched_cathegory = DatabaseApi().get_cathegory_by_id(cathegory.id)
        self.assertEqual(cathegory, fetched_cathegory)

        fetched_person: Person = DatabaseApi().get_person_by_id(0)
        self.assertTrue(len(fetched_person.cathegory_ids) == 1)
        self.assertEqual(fetched_person.cathegory_ids[0], cathegory.id)

        DatabaseApi().remove_cathegory_by_id(cathegory.id)
        fetched_person = DatabaseApi().get_person_by_id(0)
        self.assertEqual(person1, fetched_person)
        with self.assertRaises(psycopg2.ProgrammingError):
            DatabaseApi().get_cathegory_by_id(cathegory.id)

    def test_simple_insert_operation_1(self):
        self.__truncate_tables()
        person1 = Person(0, 'Amogus', [], 0)
        DatabaseApi().add_person(person1)
        cathegory = Cathegory(0, 0, DatabaseApi().get_expense_cathegory_type_id(),
                              'example_cathegory_1', 1000, 0)
        
        cathegory.id = DatabaseApi().add_cathegory(cathegory)
        money_amount = 1000
        operation = Operation(operation_type_id=DatabaseApi().get_expense_operation_type_id(),
                              person_id=person1.id,
                              cathegory_id=cathegory.id,
                              money_amount=money_amount,
                              comment='Amogus')
        DatabaseApi().add_operation(operation)
        fetched_person: Person = DatabaseApi().get_person_by_id(person1.id)
        self.assertTrue(person1.balance - money_amount == fetched_person.balance)

    def test_all_cathegories_select_1(self):
        self.__truncate_tables()
        person1 = Person(0, 'Amogus', [], 0)
        DatabaseApi().add_person(person1)
        cathegory = Cathegory(0, 0, DatabaseApi().get_expense_cathegory_type_id(),
                              'example_cathegory_1', 1000, 0)
        
        cathegory.id = DatabaseApi().add_cathegory(cathegory)
        fetched_cathegories = DatabaseApi().get_person_all_cathegories_by_id(0)
        self.assertTrue(len(fetched_cathegories) == 1)
        self.assertEqual(fetched_cathegories[0], cathegory)

    def test_all_operations_select_1(self):
        self.__truncate_tables()
        person1 = Person(0, 'Amogus', [], 0)
        DatabaseApi().add_person(person1)
        cathegory = Cathegory(0, 0, DatabaseApi().get_expense_cathegory_type_id(),
                              'example_cathegory_1', 1000, 0)
        
        cathegory.id = DatabaseApi().add_cathegory(cathegory)
        operation1 = Operation(operation_type_id=DatabaseApi().get_expense_operation_type_id(),
                              person_id=person1.id,
                              cathegory_id=cathegory.id,
                              money_amount=1000,
                              comment='Amogus1')
        operation1.id = DatabaseApi().add_operation(operation1)

        operation2 = Operation(operation_type_id=DatabaseApi().get_expense_operation_type_id(),
                              person_id=person1.id,
                              cathegory_id=cathegory.id,
                              money_amount=2000,
                              comment='Amogus2')
        operation2.id = DatabaseApi().add_operation(operation2)
        
        fetched_operations = DatabaseApi().get_person_all_operations_by_ids(0, cathegory.id)
        self.assertTrue(len(fetched_operations) == 2)
        self.assertEqual(fetched_operations[0], operation1)
        self.assertEqual(fetched_operations[1], operation2)


    def __truncate_tables(self):
        DatabaseApi().truncate_table('operation')
        DatabaseApi().truncate_table('cathegory')
        DatabaseApi().truncate_table('person')

if __name__ == '__main__':
    unittest.main()

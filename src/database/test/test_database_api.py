import unittest
from ..database_api import DatabaseApi
from ..types.person import Person 

class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        import logging_setup
        logging_setup.logging_setup()

    def test_simple_insert_person_1(self):
        person1 = Person(0, 'Amogus', [], 0)
        DatabaseApi().add_person(person1)

if __name__ == '__main__':
    unittest.main()

import datetime
import unittest
from freezegun import freeze_time

from module_03_ci_culture_beginning.homework.hw4.person import Person


class TestPerson(unittest.TestCase):
    def setUp(self) -> None:
        self.person = Person(name='test_name',
                             year_of_birth=2000,
                             address='test_address')

    def test_created_object(self):
        self.assertIsInstance(self.person, Person)
        self.assertTrue(self.person.name, 'test_name')
        self.assertIsInstance(self.person.name, str)
        self.assertTrue(self.person.year_of_birth, 2000)
        self.assertIsInstance(self.person.year_of_birth, int)
        self.assertTrue(self.person.address, 'test_address')
        self.assertIsInstance(self.person.address, str)

    def test_can_get_correct_age(self):
        with freeze_time(datetime.datetime(2023, 1, 1)):
            self.assertEqual(self.person.get_age(), 23)
            self.assertIsInstance(self.person.get_age(), int)

    def test_can_get_correct_name(self):
        self.assertEqual(self.person.get_name(), 'test_name')
        self.assertIsInstance(self.person.get_name(), str)

    def test_can_set_correct_name(self):
        self.person.set_name('set_name')
        self.assertEqual(self.person.name, 'set_name')

    def test_can_set_correct_address(self):
        self.person.set_address('set_address')
        self.assertEqual(self.person.address, 'set_address')

    def test_can_get_correct_address(self):
        self.assertEqual(self.person.get_address(), self.person.address)

    def test_can_get_is_homeless(self):
        self.assertEqual(self.person.is_homeless(), False)
        self.person.address = None
        self.assertEqual(self.person.is_homeless(), True)

    def tearDown(self) -> None:
        del self.person

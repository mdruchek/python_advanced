import json
import unittest

from module_03_ci_culture_beginning.homework.hw3.accounting import app


class TestAccounting(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.app.get('/add/20230101/100')

    def test_can_added_expenses(self):
        """
        Тест проверяет endpoint /add/ на добавление расхходов
        """
        response = self.app.get('/add/20230102/200')
        response_text = response.data.decode()
        self.assertEqual(response_text, 'Данные сохранены.')
        self.assertEqual(response.status_code, 200)
        storage = json.loads(self.app.get('/get_storage/').data.decode())
        self.assertDictEqual(storage, {'2023': {'1': {'1': 100, '2': 200, 'total': 300}, 'total': 300}})

        response = self.app.get('/add/20230102/100')
        response_text = response.data.decode()
        self.assertEqual(response_text, 'Данные сохранены.')
        self.assertEqual(response.status_code, 200)
        storage = json.loads(self.app.get('/get_storage/').data.decode())
        self.assertDictEqual(storage, {'2023': {'1': {'1': 100, '2': 300, 'total': 400}, 'total': 400}})

    def test_can_get_expenses_year(self):
        """
        Тест проверяет endpoint /calculate/<year>/ на корректное отображение информации
        """
        response = self.app.get('/calculate/2023')
        response_text = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response_text, '2023 год')
        self.assertRegex(response_text, '100 рублей')

    def test_can_get_expenses_month(self):
        """
        Тест проверяет endpoint /calculate/<year>/<month>/ на корректное отображение информации
        """
        response = self.app.get('/calculate/2023/01')
        response_text = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response_text, '.2023')
        self.assertRegex(response_text, '100 рублей')

    def test_can_added_valid_value(self):
        """
        Тест проверяет endpoint /add/ на вызов исключения при вводе не корректной даты
        """
        with self.assertRaises(ValueError):
            self.app.get('/add/20230132/200')

    def test_can_answer_if_storage_empty_year(self):
        """
        Тест проверяет endpoint /calculate/<year>/ если расходы не внесены
        """
        self.app.get('/remove_storage/')
        response = self.app.get('/calculate/2023')
        response_text = response.data.decode()
        self.assertRegex(response_text, '2023 год')
        self.assertRegex(response_text, 'не внесены.')

    def test_can_answer_if_storage_empty_month(self):
        """
        Тест проверяет endpoint /calculate/<year>/ если расходы не внесены
        """
        self.app.get('/remove_storage/')
        response = self.app.get('/calculate/2023/1')
        response_text = response.data.decode()
        self.assertRegex(response_text, '2023 год')
        self.assertRegex(response_text, 'не внесены.')

    def tearDown(self) -> None:
        self.app.get('/remove_storage/')

"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app


class TestRegistration(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = '/registration'

    def test_fields_are_valid(self):
        response = self.app.post(
            self.base_url,
            data={
                'email': 'test@exemple.ru',
                'phone': 1234567890,
                'name': 'Name',
                'address': 'address',
                'index': 123456,
                'comment': 'comment'
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_email_field_is_valid(self):
        response = self.app.post(
            self.base_url,
            data={'email': 'test@exemple.ru'}
        )
        self.assertNotIn("email': ['Invalid email address.']", response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_email_field_is_not_valid(self):
        response = self.app.post(
            self.base_url,
            data={'email': 'testexemple.ru'}
        )
        self.assertIn("'email': ['Invalid email address.']", response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_email_field_is_empty(self):
        response = self.app.post(
            self.base_url,
            data={'email': None}
        )
        self.assertIn("'email': ['This field is required.']", response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_phone_field_is_valid(self):
        response = self.app.post(
            self.base_url,
            data={'phone': '1234567890'}
        )
        self.assertNotIn("'phone': ['Длина должна быть от 10 до 10 символов.']", response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_phone_field_is_not_valid(self):
        response = self.app.post(
            self.base_url,
            data={'phone': '123456789'}
        )
        self.assertIn("'phone': ['Длина должна быть от 10 до 10 символов.']", response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_phone_field_is_empty(self):
        response = self.app.post(
            self.base_url,
            data={'phone': None}
        )
        self.assertIn("'phone': ['This field is required.']", response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_name_field_is_empty(self):
        response = self.app.post(
            self.base_url,
            data={'name': None}
        )
        self.assertIn("'name': ['This field is required.']", response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_address_field_is_empty(self):
        response = self.app.post(
            self.base_url,
            data={'address': None}
        )
        self.assertIn("'address': ['This field is required.']", response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_index_field_is_empty(self):
        response = self.app.post(
            self.base_url,
            data={'index': None}
        )
        self.assertIn("'index': ['This field is required.']", response.data.decode())
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

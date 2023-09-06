import datetime
import unittest
from freezegun import freeze_time

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class TestHelloWorldWithDay(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.base_url = '/hello-world/'
        self.days_week = ['Хорошего понедельника',
                          'Хорошего вторника',
                          'Хорошей среды',
                          'Хорошего четверга',
                          'Хорошей пятницы',
                          'Хорошей субботы',
                          'Хорошего воскресенья']

    def test_can_get_correct_day_week(self):
        username = 'username'
        start_time = datetime.datetime(2023, 9, 4)
        for days in range(7):
            with self.subTest(day=self.days_week[days]):
                current_time = start_time + datetime.timedelta(days=days)
                with freeze_time(current_time):
                    response = self.app.get(self.base_url + username)
                    response_text = response.data.decode()
                    self.assertRegex(response_text, f'\. {self.days_week[days]}\!$')

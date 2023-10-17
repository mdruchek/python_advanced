import unittest
from remote_execution import app


class TestRemoteExecution(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.url = '/run_code'
        self.app = app.test_client()

    def test_timeout_below_execution_time(self):
        response = self.app.post(
            self.url,
            data={
                "code": "import time; time.sleep(2); print('s')",
                "timeout": 1
            }
        )
        self.assertIn('Исполнение кода не уложилось в', response.text)

    def test_form_data_incorrect(self):
        test_data = (
            {
                "code": "import time; time.sleep(2); print('s')",
                "timeout": 40,
                "error": "'timeout': ['Number must be between 0 and 30.']"
            },
            {
                "code": None,
                "timeout": 5,
                "error": "'code': ['This field is required.']"
            },
            {
                "code": "import time; time.sleep(2); print('s')",
                "timeout": None,
                "error": "{'timeout': ['This field is required.']}"
            },
            {
                "code": "import time; time.sleep(2); print('s')",
                "timeout": 'a',
                "error": "{'timeout': ['Not a valid integer value.', 'Number must be between 0 and 30.']}"
            },

        )

        for num, data in enumerate(test_data):
            with self.subTest(data_nimber=num):
                response = self.app.post(
                    self.url,
                    data={
                        "code": data["code"],
                        "timeout": data["timeout"]
                    }
                )
                self.assertIn(data["error"], response.text)


if __name__ == '__main__':
    unittest.main()

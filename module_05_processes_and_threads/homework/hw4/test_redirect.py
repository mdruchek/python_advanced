import unittest
from redirect import Redirect


class TestRedirect(unittest.TestCase):
    def setUp(self) -> None:
        self.stdout_file = open('stdout.txt', 'w')
        self.stderr_file = open('stderr.txt', 'w')
        with Redirect(stdout=self.stdout_file, stderr=self.stderr_file):
            print('hello sdtout.txt')
            raise Exception('hello stderr.txt')
        self.stdout_file.close()
        self.stderr_file.close()
        self.stdout_file = open('stdout.txt', 'r')
        self.stderr_file = open('stderr.txt', 'r')

    def tearDown(self) -> None:
        self.stdout_file.close()
        self.stderr_file.close()

    def test_redirecting_stdout_stream(self):
        self.assertIn('hello sdtout.txt', self.stdout_file.read())

    def test_redirecting_stderr_stream(self):
        self.assertIn('hello stderr.txt', self.stderr_file.readlines()[-1])


if __name__ == '__main__':
    with open('test_results.txt', 'a') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)

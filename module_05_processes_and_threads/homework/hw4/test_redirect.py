import unittest
from redirect import Redirect


class TestRedirect(unittest.TestCase):
    def test_two_streams_redirected(self):
        stdout_file = open('stdout.txt', 'w')
        stderr_file = open('stderr.txt', 'w')
        with Redirect(stdout=stdout_file, stderr=stderr_file):
            print('hello sdtout.txt')
            raise Exception('hello stderr.txt')
        stdout_file.close()
        stderr_file.close()


if __name__ == '__main__':
    with open('test_results.txt', 'a') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)

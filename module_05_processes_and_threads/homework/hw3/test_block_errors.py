import unittest
from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def test_error_is_ignored(self):
        with BlockErrors(ZeroDivisionError):
            a = 1 / 0

    def test_error_thrown_higher(self):
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors(ValueError):
                a = 1 / 0

    def test_error_thrown_higher_in_the_inner_block_ignored_in_outer_one(self):
        with BlockErrors(ZeroDivisionError):
            with BlockErrors(ValueError):
                a = 1 / 0

    def test_child_errors_ignored(self):
        with BlockErrors(ArithmeticError):
            a = 1 / 0


if __name__ == '__main__':
    unittest.main()
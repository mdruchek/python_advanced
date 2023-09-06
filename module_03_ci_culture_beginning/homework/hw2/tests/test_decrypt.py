import unittest

from module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt


class TestDecrypt(unittest.TestCase):
    def setUp(self) -> None:
        self.decryption_encryption = [
            ('абра-кадабра.', 'абра-кадабра'),
            ('абраа..-кадабра', 'абра-кадабра'),
            ('абраа..-.кадабра', 'абра-кадабра'),
            ('абра--..кадабра', 'абра-кадабра'),
            ('абрау...-кадабра', 'абра-кадабра'),
            ('абра........', ''),
            ('абр......a.', 'a'),
            ('1..2.3', '23'),
            ('.', ''),
            ('1.......................', '')
        ]

    def test_encryption(self):
        for dec_enc in self.decryption_encryption:
            with self.subTest(decryption_encryption=dec_enc):
                encryption = decrypt(dec_enc[0])
                self.assertEqual(encryption, dec_enc[1])

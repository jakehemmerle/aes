import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from CryptoEngine import CryptoEngine

plaintexts = [
    'Hey this is a stirng that needs to get padded',
    'This is ano ther text string',
    'dfdfdfdfdfdfiiiiiiiiii'
]
password = 'Password!'
cipher = CryptoEngine(password)


class TestCryptoEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return

    def test_padding_1(self):
        for string in plaintexts:
            self.assertEqual(len(cipher._pad(string)) % 16, 0)


if __name__ == '__main__':
    unittest.main()

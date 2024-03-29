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
engine = CryptoEngine()


class TestCryptoEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        return

    def test_padding(self):
        for string in plaintexts:
            self.assertEqual(len(engine._pad(string)) % 16, 0)

    def test_parses_subkeys_into_16_bytes(self):
        engine.set_subkeys('data/subkeys.txt')
        print(engine.cipher.subkeys)
        for key in engine.cipher.subkeys:
            self.assertEqual(len(key), 16)


if __name__ == '__main__':
    unittest.main()

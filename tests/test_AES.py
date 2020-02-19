import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from aes import AES

cipher = AES(bytes('passwordpassword', 'utf8'))


class TestAES(unittest.TestCase):
    def test_xor(self):
        # basic
        self.assertEqual(AES._xor(bytes.fromhex('01'), bytes.fromhex('00')), bytearray.fromhex('01'))
        self.assertEqual(AES._xor(bytes.fromhex('00'), bytes.fromhex('01')), bytearray.fromhex('01'))
        # make sure length of bytes is preserved
        self.assertEqual(AES._xor(bytes.fromhex('0008'), bytes.fromhex('0004')), bytearray.fromhex('000c'))


if __name__ == '__main__':
    unittest.main()

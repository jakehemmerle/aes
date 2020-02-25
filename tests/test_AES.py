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

    def test_add_key(self):
        cipher.subkeys = [b'\x01' * 16]
        result = AES._add_key(bytearray(b'\x10' * 16), cipher.subkeys[0])
        self.assertEqual(result, bytes(b'\x11' * 16))
        self.assertNotEqual(result, bytes(b'\x00' * 16))

    def test_mix_columns(self):
        return

    def test_mix_rows(self):
        return

    def test_sub_bytes(self):
        self.assertEqual(AES._sub_bytes(bytearray(b'\x01')), bytearray(b'\x7c'))

    def test_inv_sub_bytes(self):
        self.assertEqual(AES._inv_sub_bytes(bytearray(b'\x7c')), bytearray(b'\x01'))

    def test_shift_rows(self):
        state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.assertEqual(AES._inv_shift_rows(AES._shift_rows(state)), state)


if __name__ == '__main__':
    unittest.main()

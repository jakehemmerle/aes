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
        # this is same state from lecture 5 pdf
        state = cipher._rows_to_bytes([[0x63, 0xeb, 0x9f, 0xa0],
                                       [0x2f, 0x93, 0x92, 0xc0],
                                       [0xaf, 0xc7, 0xab, 0x30],
                                       [0xa2, 0x20, 0xcb, 0x2b]])

        expected_state = cipher._rows_to_bytes([[0xba, 0x84, 0xe8, 0x1b],
                                                [0x75, 0xa4, 0x8d, 0x40],
                                                [0xf4, 0x8d, 0x06, 0x7d],
                                                [0x7a, 0x32, 0x0e, 0x5d]])

        self.assertEqual(expected_state, cipher._mix_columns(state))

    def test_sub_bytes(self):
        self.assertEqual(AES._sub_bytes(bytearray(b'\x01')), bytearray(b'\x7c'))

    def test_inv_sub_bytes(self):
        self.assertEqual(AES._inv_sub_bytes(bytearray(b'\x7c')), bytearray(b'\x01'))

    def test_shift_rows(self):
        state = bytearray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
        self.assertEqual(AES._inv_shift_rows(AES._shift_rows(state)), state)

    def test_column_conversion(self):
        state = bytearray(b'\x01\x02\x03\x04' * 4)
        self.assertEqual(cipher._columns_to_bytes(cipher._bytes_to_columns(state)), state)


if __name__ == '__main__':
    unittest.main()

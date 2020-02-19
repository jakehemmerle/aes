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
        state = bytearray([i for i in range(16)])
        print("State: {}".format(state))
        print("length of state: {}".format(len(state)))

        print("State after sub_bytes: {}".format(AES._sub_bytes(state)))
        print("len state after sub_bytes: {}".format(len(AES._sub_bytes(state))))


if __name__ == '__main__':
    unittest.main()

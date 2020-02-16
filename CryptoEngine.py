import os, json, binascii
import argon2
from aes import AES


class CryptoEngine:
    def __init__(self, secret):
        self.salt = b'superSecretSaltt!'
        self.argon2_config = {  # default values (pretty sure)
            'hash_len': 32,
            'time_cost': 2,
            'memory_cost': 102400,
            'parallelism': 8,
            'type': argon2.low_level.Type.ID
        }

        self.key = self._hash_secret(secret)[:16]   # truncate to 128-bits cause lazy
        self.cipher = AES(self.key)

    # destructor
    def __del__(self):
        return

    @staticmethod
    def _pad(plaintext: str):
        """
        Pads plaintext with 0's until it is divisible by 16-bytes.
        TODO: make last byte the number of blocks to remove (instead of just stripping all zeros)
        :param plaintext:
        :return:
        """
        plaintext = bytearray(plaintext, 'utf8')
        return plaintext + b"\x00" * (16 - len(plaintext) % 16)

    @staticmethod
    def _depad(plaintext: bytearray):
        count = 0
        for byte in reversed(plaintext):
            if byte == 0:
                count += 1
        return plaintext[:-count]

    def encrypt(self, plaintext: str):
        '''
        Pads and encrypts the plaintext
        :param plaintext:
        :return:
        '''
        padded_plaintext = self._pad(plaintext)
        ciphertext = []
        for block in self._split_to_blocks(padded_plaintext):
            ciphertext.append(self.cipher.encrypt(block))

        return ciphertext

    def decrypt(self, ciphertext):
        # returns decrypted and depadded cleartext
        return

    def _hash_secret(self, secret: str):
        """
        Extends key to 128-bit key for AES
        :param secret: secret password
        :return: 16 byte key ready for use in AES
        """
        return argon2.low_level.hash_secret_raw(str.encode(secret), self.salt, hash_len=self.argon2_config['hash_len'],
                                                time_cost=self.argon2_config['time_cost'],
                                                memory_cost=self.argon2_config['memory_cost'],
                                                parallelism=self.argon2_config['parallelism'],
                                                type=self.argon2_config['type'])

    @staticmethod
    def _split_to_blocks(data: bytearray):
        """
        Returns list of 16-byte bytearrays
        :param data:
        :return:
        """
        return [data[i:i + 16] for i in range(0, len(data), 16)]

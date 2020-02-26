import os, sys
import argon2
from aes import AES

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


class CryptoEngine:
    """
    Interface for AES engine. Allows for whole files to be encrypted, decrypted,
    and uses a KDF. Does all the padding, etc for you
    """

    def __init__(self, secret: str):
        self.salt = b'superSecretSaltt!'
        self.argon2_config = {  # default values (pretty sure)
            'hash_len': 32,
            'time_cost': 2,
            'memory_cost': 102400,
            'parallelism': 8,
            'type': argon2.low_level.Type.ID
        }

        self.key = self._hash_secret(secret)
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
        return plaintext + b"\x00" * ((16 - len(plaintext)) % 16)

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
        padded_plaintext = self._pad(plaintext[:-1])  # this -1 is only here because \n makes us use another block
        ciphertext = b''
        for block in self._split_to_blocks(padded_plaintext):
            ciphertext += self.cipher.encrypt(block)

        return ciphertext

    def decrypt(self, ciphertext):
        # returns decrypted and depadded cleartext
        return

    def _hash_secret(self, secret: str):
        """
        Extends key to 128-bit key for AES (truncates 256-bit result to 128-bit)
        :param secret: secret password
        :return: 16 byte key ready for use in AES
        """
        return argon2.low_level.hash_secret_raw(str.encode(secret), self.salt, hash_len=self.argon2_config['hash_len'],
                                                time_cost=self.argon2_config['time_cost'],
                                                memory_cost=self.argon2_config['memory_cost'],
                                                parallelism=self.argon2_config['parallelism'],
                                                type=self.argon2_config['type'])[:16]

    @staticmethod
    def _split_to_blocks(data: bytearray):
        """
        Returns list of 16-byte bytearrays
        :param data:
        :return:
        """
        return [data[i:i + 16] for i in range(0, len(data), 16)]

    def set_subkeys(self, file_location: str):
        with open(file_location, 'r') as file:
            key_string = file.read()
        subkeys = [bytes.fromhex(key) for key in key_string[:-1].split('\n')]  # -1 removes last '\n'

        self.cipher.subkeys = subkeys


if __name__ == '__main__':
    engine = CryptoEngine('defailt_password')  # password needed for initalition

    engine.set_subkeys('data/subkeys.txt')
    with open('data/plaintext.txt', 'r') as file:
        plaintext = file.read()
    ciphertext = engine.encrypt(plaintext)

    print("State after round {}: {}".format(len(engine.cipher.subkeys) - 1, ciphertext.hex()))

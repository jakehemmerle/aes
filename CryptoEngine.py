import os, sys
from aes import AES

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))


class CryptoEngine:
    """
    Interface for AES engine. Allows for whole files to be encrypted, decrypted,
    and uses a KDF. Does all the padding, etc for you
    """

    def __init__(self):
        # self.key = self._hash_secret(secret)
        self.cipher = AES()

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
    engine = CryptoEngine()

    engine.set_subkeys('data/subkeys.txt')
    with open('data/plaintext.txt', 'r') as file:
        plaintext = file.read()
    ciphertext = engine.encrypt(plaintext)

    print("State after round {}: {}".format(len(engine.cipher.subkeys) - 1, ciphertext.hex()))

    with open('data/results.txt', 'w') as file:
        file.write(ciphertext.hex())

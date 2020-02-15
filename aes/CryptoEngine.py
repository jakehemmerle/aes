import os, json, binascii
import argon2


class CryptoEngine:
    def __init__(self, secret):
        self.salt = b'superSecretSaltt!'
        self.argon2_config = {
            'hash_len': 32,
            'time_cost': 2,
            'memory_cost': 102400,
            'parallelism': 8,
            'type': argon2.low_level.Type.ID
        }

        # if database_location is ':test:':
        #     self.encrypted_db_location = 'test.db.enc'
        #
        # if database_location is not None:
        #     self.encrypted_db_location = database_location
        #     self.decrypted_db_location = database_location[-4]
        #     self.decrypt_and_write_to_disk()
        # else:
        #     self.encrypted_db_location = 'db.sqlite.enc'
        #     self.decrypted_db_location = self.encrypted_db_location[:-4]  # strip '.enc' off the end

        self.key = self._hash_secret(secret)

    # destructor
    def __del__(self):
        self.encrypt_and_write_to_disk()

    @staticmethod
    def _pad(plaintext: bytearray):
        # pads input to be divisible by 16 bytes (128-bits)
        return plaintext + b"\x00" * (16 - len(plaintext) % 16)

    @staticmethod
    def _depad(plaintext: bytearray):
        count = 0
        for byte in reversed(plaintext):
            if byte == 0:
                count += 1
        return plaintext[:-count]

    def _get_ciphertext(self, plaintext):
        # pads and encrypts the plaintext
        for block in plaintext:
        = self._pad(plaintext)
        ciphertext = self.encrypt_and_digest(plaintext)
        return ciphertext

    def _get_plaintext(self, ciphertext, tag):
        # returns decrypted and depadded cleartext
        plaintext = self.cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.rstrip(b'\0')

    # def _encode_blob(self, encrypt_and_digest):
    #     # returns an encrypted blob storing everything needed to decrypt and verify the db
    #     ciphertext, tag = encrypt_and_digest
    #     return bytes(json.dumps({
    #         'ciphertext': binascii.hexlify(ciphertext).decode('ascii'),
    #         'tag': binascii.hexlify(tag).decode('ascii'),
    #         'nonce': binascii.hexlify(self.cipher.nonce).decode('ascii')
    #     }), 'utf-8')

    # @staticmethod
    # def _decode_blob(blob):
    #     message = json.loads(blob)
    #     return binascii.unhexlify(message['ciphertext']), binascii.unhexlify(message['tag']), binascii.unhexlify(
    #         message['nonce'])

    @staticmethod
    def _delete_file(filename):
        if os.path.isfile(filename):
            os.remove(filename)
        else:
            print("Could Not Delete")

    def _hash_secret(self, secret: str):
        """
        Computes a deterministic Argon2 hash using a predefined salt
        :param secret: secret password
        :return: 16 bytes hash ready for use in AES engine
        """
        return argon2.low_level.hash_secret_raw(str.encode(secret), self.salt, hash_len=self.argon2_config['hash_len'],
                                                time_cost=self.argon2_config['time_cost'],
                                                memory_cost=self.argon2_config['memory_cost'],
                                                parallelism=self.argon2_config['parallelism'],
                                                type=self.argon2_config['type'])

    # def decrypt_and_write_to_disk(self):
    #     try:
    #         with open(self.encrypted_db_location, 'rb') as encrypted_db_file:
    #             blob = encrypted_db_file.read()
    #
    #         ciphertext, tag, nonce = self._decode_blob(blob)
    #         self.cipher.nonce = nonce
    #         plaintext = self._get_plaintext(ciphertext, tag)
    #
    #         self._delete_file(self.decrypted_db_location)
    #         with open(self.decrypted_db_location, 'wb') as decrypted_db_file:
    #             decrypted_db_file.write(plaintext)
    #     except IOError:
    #         print("No encrypted database. Creating new DB.")

    # def encrypt_and_write_to_disk(self, encrypted_db_location=None):
    #     """
    #     Encrypt the open database file and write to disk
    #     :param encrypted_db_location:  optional "Save as..."
    #     :return:
    #     """
    #     if encrypted_db_location is ':test:':
    #         encrypted_db_location = 'test.db.enc'
    #     if encrypted_db_location is None:
    #         encrypted_db_location = self.encrypted_db_location
    #     with open(self.decrypted_db_location, 'rb') as decrypted_db_file:
    #         plaintext = decrypted_db_file.read()
    #     blob = self._encode_blob(self._get_ciphertext_and_tag(plaintext))
    #     with open(encrypted_db_location, 'wb') as encrypted_db_file:
    #         encrypted_db_file.write(blob)
    #         print("Write successful.")
    #     self._delete_file(self.decrypted_db_location)

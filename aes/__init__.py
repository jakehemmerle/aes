class AES:
    '''
    Key length
    '''

    def __init__(self, key: bytes):
        assert len(key) == 16
        self.key = key
        self.subkeys = []

    def _manually_set_subkeys(self, subkeys: list):
        self.subkeys = subkeys

    def encrypt(self, plaintext_block: bytearray):
        '''
        Returns block encrypted with key
        :param plaintext_block:
        :return:
        '''
        state = plaintext_block
        self._add_key(state)

    def _add_key(self, block: bytearray):

        return

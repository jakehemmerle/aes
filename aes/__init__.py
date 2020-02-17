class AES:
    '''
    Key length
    '''

    def __init__(self, key: bytes):
        assert len(key) == 16
        self.key = key
        self.subkeys = []

    @staticmethod
    def _xor(a, b):
        '''
        :param a: bytes or bytearray
        :param b: bytes or bytearray
        :return: bytearray
        '''
        return bytearray([c ^ d for c, d in zip(a, b)])

    def _manually_set_subkeys(self, subkeys: list):
        '''
        Manually sets subkeys
        :param subkeys:
        :return: None
        '''
        self.subkeys = subkeys

    def encrypt(self, plaintext_block: bytearray):
        '''
        Returns block encrypted with key
        :param plaintext_block:
        :return:
        '''
        state = plaintext_block
        for key in self.subkeys:
            self._add_key(state, key)

    @staticmethod
    def _add_key(block: bytearray, key: bytes):
        return AES._xor(block, key)

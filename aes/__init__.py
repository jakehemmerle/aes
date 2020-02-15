class AES:
    '''
    Key length
    '''
    def __init__(self, key: bytes):
        assert len(key) == 16
        self.key = key

    def encrypt(self, plaintext_block: bytearray):
        '''
        Returns block encrypted with instance key
        :param block:
        :return:
        '''

        block = plaintext_block

        self._initial_permutation(block)



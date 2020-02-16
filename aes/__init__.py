class AES:
    '''
    Key length
    '''
    def __init__(self, key: bytes):
        assert len(key) == 16
        self.key = key

    def encrypt(self, plaintext_block: bytearray):
        '''
        Returns block encrypted with key
        :param plaintext_block:
        :return:
        '''
        state = plaintext_block
        self._initial_permutation(state)


    def _initial_permutation(self, block: bytearray):
        # TODO
        return

class BlockNotLinkedError(Exception):
    '''
    An Exception Class to be raised when The Current Block Has No Previous Hash
    GenesisBlock has default Hash 0000
    '''
    pass

# Not yet used
class BlockCorruptedError(Exception):
    '''
    An Exception Class to be raised when some data has been tampered by someone
    '''
    pass

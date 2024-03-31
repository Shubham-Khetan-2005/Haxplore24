from .errors import BlockNotLinkedError
import hashlib
import time


class Block:
    """
    A class for Making A Block In A Blockchain

    ...

    Attributes
    ----------
    t : struct_time
        A variable storing localtime on time of creaton of the block
    timeStamp : str
        A string containing localtime in DD/MM/YYYY hh:mm:ss tt 
        Example: 2/2/2021 7:22:47 AM

        This variable is used to distinguish 
        2 different blocks with similar transactions,
        else they would have the same hash.

    previousHash : str
        The hash of previous block
    transactions : list
        A list of all transactions 
    hash : str
        The hash of current block
        initially None, and is assigned value while mining block
    nonce : int
        An int variable for changing current blocks hash to meet certain conditions in hash.
        This process can be considered mining as it takes exponential time when difficulty of mining increases


    Methods
    -------
    generateHash():
        returns the current Block's Hash
    mineBlock():
        a function for proof of work or mining current block

    """

    def __init__(self, transactions: list, previousHash: str = "") -> None:
        """
        Parameters
        ----------
        transactions : list
            A list of all transactions
        previousHash : str
            The hash of previous block
            default:""
        ---------- 
        """
        self.t = time.localtime()
        self.timeStamp = f"{self.t.tm_mday}/{self.t.tm_mon}/{self.t.tm_year} {self.t.tm_hour if self.t.tm_hour<=12 else self.t.tm_hour-12}:{self.t.tm_min}:{self.t.tm_sec} {'AM' if self.t.tm_hour<=12 else 'PM'}"
        self.previousHash = previousHash
        self.transactions = transactions
        self.nonce = 0
        self.hash = None

    def generateHash(self) -> str:
        """
        Generates hash of current block and returns it

        Raises
        ------
        BlockNotLinkedError
            if the current block is not linked to any blockchain,
            i.e. when it's previous hash is empty
        ------
        """
        if self.previousHash == "":
            raise BlockNotLinkedError(
                "Current block not linked with blockchain")
        return hashlib.sha256(f"{self.previousHash}{self.timeStamp}{self.transactions}{self.nonce}".encode()).hexdigest()

    def hasValidTransactions(self,public_key):
        """
        Function to check if all trnsaction in self.transactions are valid and signed by sender
        Parameter
        ---------
        public_key : PublicKey
            the public key of the user's bitcoin wallet
        """
        for tx in self.transactions:
            if not tx.isValid(public_key):
                return False

        return True

    # Proof Of Work Or Mining Block of BlockChain
    def mineBlock(self, difficulty: int,public_key) -> None:
        """
        A function for proof of work or mining of block

        the mining process: 
            after every increment in nonce value,a new hash value is generated
            if the new hash contains (difficulty) times 0 at start then 
            the block is said to be mined...
            Example:
            mineBlock(3):
                requirs hash to be something like:
                000XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

        Parameters
        ----------
        difficulty : int
            it is the number of 0s at beginning of hash...
        """
        self.hash = self.generateHash()
        if not self.hasValidTransactions(public_key):
            raise Exception("Some transactions are not valid in current Block")
        while self.hash[:difficulty] != "0"*difficulty:
            self.nonce += 1
            self.hash = self.generateHash()


    def __repr__(self) -> str:
        return str({"timestamp": self.timeStamp, "transactions": self.transactions, "previousHash": self.previousHash, "hash": self.hash})

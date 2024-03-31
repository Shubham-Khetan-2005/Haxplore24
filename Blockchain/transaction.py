import hashlib

def to_string(key,isPublic):
    if isPublic:
        return key.to_pem()[len(b"-----BEGIN PUBLIC KEY-----\n"):-len(b"\n-----END PUBLIC KEY-----\n")].decode()
    return key.to_pem()[len(b"-----BEGIN EC PRIVATE KEY-----\n"):-len(b"\n-----END EC PRIVATE KEY-----\n")].decode()

def remove_escapeChar(word):
    res=""
    for i in word:
        if i not in ['\n','\t','\r','\b']:
            res+=i

    return res
    
class Transaction:
    """
    A Class Containing All Transaction information
    Attributes
    ----------
    amount : int
        the number of coins being transacted
    sentFrom : str
        the address of user sending amount
    sentTo : str
        the address of user receiving amount

    """

    def __init__(self, sentFrom: str, sentTo: str, amount: int) -> None:
        """
        Parameters
        ----------
        amount : int
            the number of coins being transacted
        sentFrom : str
            the address of user sending amount
        sentTo : str
            the address of user receiving amount
        ----------
        """
        self.sentFrom = sentFrom
        self.sentTo = sentTo
        self.amount = amount
        self.signature = None
        self.txHash = None

    def generateHash(self) -> str:
        return hashlib.sha256(f"{self.sentFrom}{self.sentTo}{self.amount}".encode()).hexdigest()

    def sign(self, signing_keypair:tuple):
        """
        Parameters
        ----------
        signing_keypair: tuple[2]
            contains pair of keys (private_key,public_key)
        """
        pvt_key,pub_key=signing_keypair
        if remove_escapeChar(to_string(pub_key,True)) != self.sentFrom:
            raise Exception(f"You Cannot Sign transaction for other's wallets: \n{remove_escapeChar(to_string(pub_key,True))} != \n{self.sentFrom}")
        self.txHash = self.generateHash()
        self.signature = pvt_key.sign(self.txHash.encode())

    def isValid(self, public_key):
        """
        Validates the transaction if it is signed by sender or it is a reward transaction or none of these
        Parameter
        ---------
        public_key : PublicKey
            the public key of the user
        """
        if self.sentFrom == "SYSTEM":
            return True

        if not self.signature or not len(self.signature):
            raise Exception("Transaction Not Signed")

        valid = public_key.verify(self.signature, self.txHash.encode())
        return valid

    def __repr__(self) -> str:
        return str({"sentFrom": str(self.sentFrom), "sentTo": str(self.sentTo), "amount": self.amount})

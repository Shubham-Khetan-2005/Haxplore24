from .block import Block
from .transaction import Transaction

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
    
class BlockChain:
    """
A class for Making A Block In A Blockchain

    ...

    Attributes
    ----------
    pendingTransactions : list
        A variable storing all the pending transactions to be executed by next block
    chain : list
        A list Representing the Blockchain containing Genesis Block(first block without transaction)
        
    difficulty : int
        The difficulty of mining a block
        refer Block.mineBlock function for detail
    miningReward : int
        The Number of coins a miner gets as rewrd for mining a block

    Methods
    -------
    createGenesisBlock():
        returns A Genesis Block
    getLatestBlock():
        returns The Last Block in blockchain
    minePendingTransactions():
        fills a new block with all pending transactions,
        mines it and then adds it to bockchain.
    addTransaction(transaction):
        adds new transaction in pendingTransactions list
    getBalanceOfAddress(address):
        returns balance of user (address)
    isChainValid():
        checks for data tamper in Blockchain, 
        returns true if valid and false if some data is tampered
    """
    def __init__(self) -> None:
        self.pendingTransactions=[]
        self.chain=[self.createGenesisBlock()]     
        self.difficulty=3
        # Miners Get coins as reward on mining a new block...
        self.miningReward=100

    def createGenesisBlock(self)->Block:
        """
        creates A Genesis Block and returns it
        """
        genBlock=Block([Transaction("SYSTEM","SYSTEM",0)],previousHash="0000")
        genBlock.hash=genBlock.generateHash()
        return genBlock



    def getLatestBlock(self)->Block:
        """
        returns The Last Block in blockchain
        """
        return self.chain[-1]

    def minePendingTransactions(self,miningRewardAddress)->None:
        """
        fills a new block with all pending transactions,
        mines it and then adds it to bockchain.
                Parameter
        ---------
        miningRewardAddress : PublicKey
            the public key of the user's bitcoin wallet
        """
        block=Block(transactions=self.pendingTransactions,previousHash=self.getLatestBlock().hash)
        block.mineBlock(self.difficulty,miningRewardAddress)

        print(f"Block Successfully mined...")
        self.chain.append(block)
        # adding the miningreward to the user who mined current block
        self.pendingTransactions=[
            Transaction("SYSTEM",remove_escapeChar(to_string(miningRewardAddress,True)),self.miningReward)
        ]

    def addTransaction(self,transaction:Transaction,public_key)->None:
        """
        adds new transaction in pendingTransactions list
        """
        if not transaction.sentFrom or not transaction.sentTo:
            raise Exception("Transaction Must Contain From and To Address");
        if not transaction.isValid(public_key):
            raise Exception("Cannot add invalid transaction to chain")
        self.pendingTransactions.append(transaction)

    def getBalanceOfAddress(self,address:str,initBalance=0)->int:
        """
        returns balance of user (address)
                Parameter
        ---------
        address : PublicKey
            the public key of the user's bitcoin wallet whose balance is to be calculated
        """
        balance=int(initBalance)

        for block in self.chain:
            for t in block.transactions:
                if t.sentFrom==address:
                    balance-=int(t.amount)
                if t.sentTo==address:
                    balance+=int(t.amount)
        return balance
        
    # Adding A Block Without Reward
    # Not in use
    def addBlock(self,newBlock:Block)->None:
        newBlock.previousHash=self.getLatestBlock().hash
        newBlock.mineBlock(self.difficulty)
        self.chain.append(newBlock)

    def isChainValid(self,public_key)->bool:
        """
        checks for data tamper in Blockchain, 
        returns true if valid and false if some data is tampered
        Parameter
        ---------
        public_key : PublicKey
            the public key of the user's bitcoin wallet
        """
        for i in range(1,len(self.chain)):
            currentBlock=self.chain[i]
            prevBlock=self.chain[i-1]
            if not currentBlock.hasValidTransactions(public_key=public_key):
                return False
            # Checks for change in data in current block
            if currentBlock.hash!=currentBlock.generateHash():
                return False
            # Checks for broken link if the hash has been regenerated
            if currentBlock.previousHash!=prevBlock.hash:
                return False
        return True

    def __repr__(self) -> str:
        return str({"BlockChain":{i:item for i,item in enumerate(self.chain)}})
import datetime
import hashlib

from src import transactions

difficulty = 5

class Block:
    def __init__(self, data, previousHash, address, timestamp = datetime.datetime.now().timestamp()):
        self.data = data
        self.previousHash = previousHash
        self.timestamp = timestamp

        self.nonce = 0
        self.hash = ""

        self.mine(address)
      
    def calculateHash(self):
        self.hash = hashlib.sha256((
            str(self.data) + str(self.previousHash) + str(self.timestamp) + str(self.nonce)
        ).encode("utf-8")).hexdigest()
    
    def mine(self, address):
        self.data.insert(0, {
            "type": "transaction",
            "body": transactions.newReward("0" * 128)
        })

        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1

            self.calculateHash()

class Blockchain:
    def __init__(self):
        self.blocks = []

    def append(self, block):
        # TODO: Add verification, maybe even move to new method

        self.blocks.append(block)
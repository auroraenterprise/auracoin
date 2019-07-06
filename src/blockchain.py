import datetime
import hashlib
import re

from src import transactions
from src.base40 import Base40

difficulty = 5

class ValidationError(Exception):
    pass

class Block:
    def __init__(self, data, previousHash, address, timestamp = datetime.datetime.now().timestamp()):
        self.data = data
        self.previousHash = previousHash
        self.timestamp = timestamp

        self.nonce = 0
        self.hash = ""

        self.mine(address)
    
    def getHashCalculation(self):
        return hashlib.sha256((
            str(self.data) + str(self.previousHash) + str(self.timestamp) + str(self.nonce)
        ).encode("utf-8")).hexdigest()
      
    def calculateHash(self):
        self.hash = self.getHashCalculation()
    
    def mine(self, address):
        self.data.insert(0, {
            "type": "transaction",
            "body": transactions.newReward(address)
        })

        while not self.hash.startswith("0" * difficulty):
            self.nonce += 1

            self.calculateHash()

class Blockchain:
    def __init__(self):
        self.blocks = []

    def append(self, block):
        self.blocks.append(block)
    
    def verify(self, verbose = True):
        lastTimestamp = 0
        transactionNonces = {}
        registeredAddresses = {
            transactions.COINBASE_ADDRESS: transactions.COINBASE_PUBLIC_KEY
        }

        for i in range(0, len(self.blocks)):
            if verbose: print("- Validating block " + str(i) + " of " + str(len(self.blocks)) + " in blockchain... (" + str((i / len(self.blocks)) * 100) + "%)")

            thisBlock = self.blocks[i]

            if i == 0:
                previousBlock = None
            else:
                previousBlock = self.blocks[i - 1]
            
            if thisBlock.__init__.__code__ != Block.__init__.__code__ or thisBlock.getHashCalculation.__code__ != Block.getHashCalculation.__code__ or thisBlock.calculateHash.__code__ != Block.calculateHash.__code__ or thisBlock.mine.__code__ != Block.mine.__code__:
                raise ValidationError("block " + str(i) + " has different class methods")

            if thisBlock.timestamp <= lastTimestamp:
                raise ValidationError("block " + str(i) + " has invalid timestamp")

            lastTimestamp = thisBlock.timestamp

            if i > 0:
                if thisBlock.previousHash != previousBlock.hash:
                    raise ValidationError("block " + str(i) + " has invalid previousHash")
                
            if thisBlock.hash != thisBlock.getHashCalculation():
                raise ValidationError("block " + str(i) + " has invalid hash")
            
            minerAlreadyRewarded = False
            
            for d in range(0, len(thisBlock.data)):
                if verbose: print("    - Verifying data " + str(d) + " of " + str(len(thisBlock.data)) + " in block " + str(i) + " of " + str(len(self.blocks)) + "... (" + str((i / len(self.blocks)) * 100) + "% > " + str((d / len(thisBlock.data)) * 100) + "%)")

                thisData = thisBlock.data[d]

                if thisData["type"] == "data":
                    pass
                elif thisData["type"] == "transaction":
                    thisTransaction = thisData["body"]

                    if thisData["body"].verify() != True:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (invalid signature)")

                    if thisTransaction.sender in transactionNonces:
                        if thisTransaction.nonce in transactionNonces[thisTransaction.sender]:
                            raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (reused nonce)")
                        else:
                            transactionNonces[thisTransaction.sender].append(thisTransaction.nonce)
                    else:
                        transactionNonces[thisTransaction.sender] = [thisTransaction.nonce]
                    
                    if thisTransaction.sender == transactions.COINBASE_ADDRESS and thisTransaction.senderPublicKey == transactions.COINBASE_PUBLIC_KEY and not minerAlreadyRewarded:
                        minerAlreadyRewarded = True
                    elif thisTransaction.sender == transactions.COINBASE_ADDRESS and thisTransaction.senderPublicKey == transactions.COINBASE_PUBLIC_KEY:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (miner already rewarded)")
                    elif thisTransaction.sender == transactions.COINBASE_ADDRESS:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (wrong public key for coinbase issued)")
                    
                    if thisTransaction.sender in registeredAddresses:
                        if registeredAddresses[thisTransaction.sender] != thisTransaction.senderPublicKey and i != 0:
                            raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (wrong public key for sender issued)")
                    elif thisTransaction.sender != transactions.COINBASE_ADDRESS:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (sender address doesn't exist)")
                    
                    if thisTransaction.receiver not in registeredAddresses:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (receiver address doesn't exist)")
                elif thisData["type"] == "registration":
                    thisRegistration = thisData["body"]

                    if thisRegistration["address"] in registeredAddresses:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid registration (address already registered)")

                    if not re.match("[" + Base40().digits + "]*$", thisRegistration["address"]):
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid registration (invalid address digits)")
                    
                    if len(thisRegistration["publicKey"]) != 128:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid registration (incorrect publicKey length)")
                else:
                    raise ValidationError("block " + str(i) + " data " + str(d) + " is of an invalid data type (\"" + thisData["type"] + "\")")

                # TODO: Add block difficulty calculations

def newAddress(previousHash, timestamp = datetime.datetime.now().timestamp()):
    info = transactions.newAddress()

    return (
        Block([{
            "type": "registration",
            "body": {
                "address": info["address"],
                "publicKey": info["publicKey"]
            }
        }], previousHash, transactions.COINBASE_ADDRESS, timestamp),
        info
    )
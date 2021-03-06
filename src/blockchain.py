# Auracoin
# 
# Copyright (C) Aurora Enterprise. All Rights Reserved.
# 
# https://aur.xyz
# Licensed by the Aurora Open-Source Licence, which can be found at LICENCE.md.

import datetime
import hashlib
import re

from src import transactions
from src.base40 import Base40

INITIAL_DIFFICULTY = 1
INITIAL_DIFFICULTY_TARGET = ((2 ** 16) - 1) * (2 ** 218)
TARGET_SOLVE_TIME = 120 # 2 minutes in seconds
TARGET_BLOCKS_SOLVED = 1440 # Should last for 2 days

class ValidationError(Exception):
    pass

def calculateTarget(initialDifficultyTarget, difficulty):
    return initialDifficultyTarget / difficulty

def calculateNextDifficulty(difficulty, solveTime):
    return difficulty * (TARGET_SOLVE_TIME / solveTime)

class Block:
    def __init__(self, data, previousHash, address, difficulty, mine = True):
        self.data = data
        self.previousHash = previousHash
        self.difficulty = difficulty
        self.timestamp = datetime.datetime.utcnow().timestamp()

        self.nonce = 0
        self.hash = ""

        if mine:
            self.mine(address)
    
    def getHashCalculation(self):
        dataString = ""

        for item in self.data:
            if item["type"] == "registration":
                dataString += item["type"] + item["body"]["address"] + item["body"]["publicKey"]
            else:
                dataString += item["type"] + str(item["body"])

        return hashlib.sha256((
            dataString + str(self.previousHash) + str(self.timestamp) + str(self.difficulty) + str(self.nonce)
        ).encode("utf-8")).hexdigest()
      
    def calculateHash(self):
        self.hash = self.getHashCalculation()
    
    def mine(self, address):
        self.data.insert(0, {
            "type": "transaction",
            "body": transactions.newReward(address)
        })

        self.calculateHash()

        target = calculateTarget(INITIAL_DIFFICULTY_TARGET, self.difficulty)

        while int(self.hash, 16) > target:
            self.nonce += 1

            self.calculateHash()
        
class Blockchain:
    def __init__(self):
        self.blocks = []
        self.difficulty = INITIAL_DIFFICULTY

    def append(self, block):
        self.blocks.append(block)

        if len(self.blocks) > 1 and len(self.blocks) % TARGET_BLOCKS_SOLVED == 0:
            summedTimeTaken = 0
            oldDifficulty = self.difficulty

            for i in range(1, TARGET_BLOCKS_SOLVED):
                summedTimeTaken += self.blocks[-i].timestamp - self.blocks[-(i + 1)].timestamp

            self.difficulty = calculateNextDifficulty(self.difficulty, summedTimeTaken / TARGET_BLOCKS_SOLVED)

            if self.difficulty < oldDifficulty / 4:
                self.difficulty = oldDifficulty / 4
            
            if self.difficulty > oldDifficulty * 4:
                self.difficulty = oldDifficulty * 4
    
    def verify(self, verbose = False):
        lastTimestamp = 0
        transactionNonces = {}
        registeredAddresses = {
            transactions.COINBASE_ADDRESS: transactions.COINBASE_PUBLIC_KEY
        }
        addressBalances = {
            transactions.COINBASE_ADDRESS: 0
        }

        for i in range(0, len(self.blocks)):
            if verbose: print("- Verifying block " + str(i) + " (" + str(i + 1) + "/" + str(len(self.blocks)) + ") in blockchain... (" + str((i / len(self.blocks)) * 100) + "%)")

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
                raise ValidationError("block " + str(i) + " has invalid hash (wrong hash calculated)")
            
            if int(thisBlock.hash, 16) > calculateTarget(INITIAL_DIFFICULTY_TARGET, thisBlock.difficulty):
                raise ValidationError("block " + str(i) + " has invalid hash (hash does not adhere to target)")
            
            minerAlreadyRewarded = False
            
            for d in range(0, len(thisBlock.data)):
                if verbose: print("    - Verifying data " + str(d) + " (" + str(d + 1) + "/" + str(len(thisBlock.data)) + ") in block " + str(i) + " (" + str(i + 1) + "/" + str(len(self.blocks)) + ")... (" + str((i / len(self.blocks)) * 100) + "% > " + str((d / len(thisBlock.data)) * 100) + "%)")

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
                    
                    if thisTransaction.sender == transactions.COINBASE_ADDRESS and thisTransaction.senderPublicKey == transactions.COINBASE_PUBLIC_KEY and thisTransaction.amount == transactions.BLOCK_REWARD and not minerAlreadyRewarded:
                        addressBalances[thisTransaction.sender] += transactions.BLOCK_REWARD
                        minerAlreadyRewarded = True
                    elif thisTransaction.sender == transactions.COINBASE_ADDRESS and thisTransaction.senderPublicKey == transactions.COINBASE_PUBLIC_KEY and thisTransaction.amount == transactions.BLOCK_REWARD:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (miner already rewarded)")
                    elif thisTransaction.sender == transactions.COINBASE_ADDRESS and thisTransaction.senderPublicKey == transactions.COINBASE_PUBLIC_KEY:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (miner reward different from block reward)")
                    elif thisTransaction.sender == transactions.COINBASE_ADDRESS:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (wrong public key for coinbase issued)")
                    
                    if thisTransaction.sender in registeredAddresses:
                        if registeredAddresses[thisTransaction.sender] != thisTransaction.senderPublicKey and i != 0:
                            raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (wrong public key for sender issued)")
                    elif thisTransaction.sender != transactions.COINBASE_ADDRESS:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (sender address doesn't exist)")
                    
                    if thisTransaction.receiver not in registeredAddresses:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (receiver address doesn't exist)")
                    
                    if thisTransaction.amount <= 0:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (invalid amount)")
                    
                    if thisTransaction.sender != transactions.COINBASE_ADDRESS:
                        if addressBalances[thisTransaction.sender] < thisTransaction.amount:
                            raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid transaction (sender has insufficient balance)")
                        else:
                            addressBalances[thisTransaction.sender] -= thisTransaction.amount
                    
                    addressBalances[thisTransaction.receiver] += thisTransaction.amount
                elif thisData["type"] == "registration":
                    thisRegistration = thisData["body"]

                    if thisRegistration["address"] in registeredAddresses:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid registration (address already registered)")

                    if not re.match("[" + Base40().digits + "]*$", thisRegistration["address"]):
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid registration (invalid address digits)")
                    
                    if len(thisRegistration["publicKey"]) != 128:
                        raise ValidationError("block " + str(i) + " data " + str(d) + " is an invalid registration (incorrect publicKey length)")
                    
                    registeredAddresses[thisRegistration["address"]] = thisRegistration["publicKey"]
                    addressBalances[thisRegistration["address"]] = 0
                else:
                    raise ValidationError("block " + str(i) + " data " + str(d) + " is of an invalid data type (\"" + thisData["type"] + "\")")

def newAddress(previousHash, difficulty):
    info = transactions.newAddress()

    return (
        Block([{
            "type": "registration",
            "body": {
                "address": info["address"],
                "publicKey": info["publicKey"]
            }
        }], previousHash, transactions.COINBASE_ADDRESS, difficulty),
        info
    )

def newAddressFromPublicKey(publicKey, previousHash, difficulty):
    info = transactions.newAddressFromPublicKey(publicKey)

    return (
        Block([{
            "type": "registration",
            "body": {
                "address": info["address"],
                "publicKey": info["publicKey"]
            }
        }], previousHash, transactions.COINBASE_ADDRESS, difficulty),
        info
    )
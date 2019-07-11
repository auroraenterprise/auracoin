import os
import json

from src import transactions, storage, transactions

nodeBlockchain = None
nodeRequests = []

def checkAddress(address):
    try:
        for block in nodeBlockchain.blocks:
            for item in block.data:
                if item["type"] == "registration":
                    if item["body"]["address"] == address:
                        return item["body"]["publicKey"]
        
        return None
    except:
        return None

def checkBalance(address):
    amount = 0

    try:
        for block in nodeBlockchain.blocks:
            for item in block.data:
                if item["type"] == "transaction":
                    if item["body"].sender == address:
                        amount -= item["body"].amount
                    elif item["body"].receiver == address:
                        amount += item["body"].amount
        
        return amount
    except:
        return 0

def getBlockchain():
    blocks = []
    difficulty = nodeBlockchain.difficulty

    for block in nodeBlockchain.blocks:
        data = []

        for item in block.data:
            if isinstance(item["body"], transactions.Transaction):
                data.append({
                    "type": item["type"],
                    "body": item["body"].__dict__
                })
            else:
                data.append({
                    "type": item["type"],
                    "body": item["body"]
                })

        blocks.append({
            "data": data,
            "address": block.address,
            "previousHash": block.previousHash,
            "difficulty": block.difficulty,
            "timestamp": block.timestamp,
            "nonce": block.nonce,
            "hash": block.hash
        })

    return json.dumps({
        "blocks": blocks,
        "difficulty": difficulty
    })

def handleData(data, verbose = False):
    nodeRequests.append({
        "type": "data",
        "body": data
    })

    if verbose: print("- New request for data added")

    return "Status/ok"

def handleTransaction(sender, senderPublicKey, receiver, amount, certificate, signature, nonce, verbose = False):
    if checkAddress(sender) == None:
        return "Status/fail/exist"
    
    if checkAddress(receiver) == None:
        return "Status/fail/exist"

    if checkBalance(sender) < amount:
        return "Status/fail/balance"

    transaction = transactions.Transaction(sender, senderPublicKey, receiver, amount, certificate, signature, nonce)

    if transaction.verify():
        if verbose: print("- New request for transaction added")

        nodeRequests.append({
            "type": "transaction",
            "body": transaction
        })

        return "Status/ok"
    else:
        if verbose: print("- New request for transaction failed to verify, skipped")

        return "Status/fail/verification"
    
def handleRegistration():
    info = transactions.newAddress()

    if checkAddress(info["address"]) != None:
        return "Status/fail/exist"

    nodeRequests.append({
        "type": "registration",
        "body": {
            "address": info["address"],
            "publicKey": info["publicKey"]
        }
    })

    return "Registration/{}/{}/{}".format(info["address"], info["publicKey"], info["privateKey"])
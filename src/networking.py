# Auracoin
# 
# Copyright (C) Aurora Enterprise. All Rights Reserved.
# 
# https://aur.xyz
# Licensed by the Aurora Open-Source Licence, which can be found at LICENCE.md.

import os
import json

from src import transactions, storage, transactions

nodeBlockchain = None
nodeRequests = []

def checkAddress(address):
    try:
        # Check for blocks on the blockchain
        for block in nodeBlockchain.blocks:
            for item in block.data:
                if item["type"] == "registration":
                    if item["body"]["address"] == address:
                        return item["body"]["publicKey"]

        # Check for blocks not yet added to the blockchain
        for item in nodeRequests:
            if item["type"] == "registration":
                if item["body"]["address"] == address:
                    return item["body"]["publicKey"]
        
        return None
    except:
        return None

def checkBalance(address):
    amount = 0

    try:
        # Check for blocks on the blockchain
        for block in nodeBlockchain.blocks:
            for item in block.data:
                if item["type"] == "transaction":
                    if item["body"].sender == address:
                        amount -= item["body"].amount
                    elif item["body"].receiver == address:
                        amount += item["body"].amount
        
        # Check for blocks not yet added to the blockchain
        for item in nodeRequests:
            if item["type"] == "transaction":
                if item["body"].sender == address:
                    amount -= item["body"].amount
                elif item["body"].receiver == address:
                    amount += item["body"].amount
        
        return amount
    except:
        return 0

def checkTransactionNonceExists(address, nonce):
    try:
        # Check for blocks on the blockchain
        for block in nodeBlockchain.blocks:
            for item in block.data:
                if item["type"] == "transaction":
                    if item["body"].sender == address and item["body"].nonce == nonce:
                        return True
        
        # Check for blocks not yet added to the blockchain
        for item in nodeRequests:
            if item["type"] == "transaction":
                if item["body"].sender == address and item["body"].nonce == nonce:
                    return True
        
        return False
    except:
        return False

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
    if sender == transactions.COINBASE_ADDRESS:
        return "Status/fail/lazysod"
        
    if checkAddress(sender) == None:
        return "Status/fail/exist"
    
    if checkAddress(receiver) == None:
        return "Status/fail/exist"

    if checkBalance(sender) < amount:
        return "Status/fail/balance"
    
    if checkTransactionNonceExists(sender, nonce):
        return "Status/fail/nonce"

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

def handleRegistrationFromPublicKey(publicKey):
    if len(publicKey) != 128:
        return "Status/fail/format"

    try:
        info = transactions.newAddressFromPublicKey(publicKey)

        nodeRequests.append({
            "type": "registration",
            "body": {
                "address": info["address"],
                "publicKey": info["publicKey"]
            }
        })

        return "RegistrationFromPublicKey/{}/{}".format(info["address"], info["publicKey"])
    except:
        return "Status/fail/generation"

    if checkAddress(info["address"]) != None:
        return "Status/fail/exist"
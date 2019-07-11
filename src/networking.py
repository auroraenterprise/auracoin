import os

from src import storage, transactions

nodeBlockchain = None
nodeRequests = []

def getBlockchain():
    file = open(os.path.join(storage.CONFIG_FOLDER, "blockchain.auo"), "rb")
    returns = file.read()

    file.close()

    return returns

def handleData(data, verbose = False):
    nodeRequests.append({
        "type": "data",
        "body": data
    })

    if verbose: print("- New request for data added")

    return "Status/ok"

def handleTransaction(sender, senderPublicKey, receiver, amount, certificate, signature, nonce, verbose = False):
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

    nodeRequests.append({
        "type": "registration",
        "body": {
            "address": info["address"],
            "publicKey": info["publicKey"]
        }
    })

    return "Registration/{}/{}/{}".format(info["address"], info["publicKey"], info["privateKey"])
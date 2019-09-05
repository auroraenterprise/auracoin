# Auracoin
# 
# Copyright (C) Aurora Enterprise. All Rights Reserved.
# 
# https://aur.xyz
# Licensed by the Auracoin Open-Source Licence, which can be found at LICENCE.md.

from src import blockchain, storage

nodeBlockchain = blockchain.Blockchain()

nodeBlockchain.append(blockchain.Block(
    data = [{
        "type": "data",
        "body": input("Choose a message to write to genesis block with: ")
    }],
    previousHash = "0" * 64,
    address = "0" * 10,
    difficulty = blockchain.INITIAL_DIFFICULTY
))

print("Mined genesis block.")

myAddressInfo = blockchain.newAddress(nodeBlockchain.blocks[-1].hash, nodeBlockchain.difficulty)

nodeBlockchain.append(myAddressInfo[0])

print("Mined address creation block.")

print(nodeBlockchain.blocks, nodeBlockchain.blocks[-1].data, nodeBlockchain.blocks[-1].hash)

nodeBlockchain.verify(True)

storage.saveObject(nodeBlockchain, "blockchain")

print("Your blockchain is ready! It has been stored as ~/.auracoin/blockchain.auo.")
print("Your address:    " + myAddressInfo[1]["address"])
print("Your publicKey:  " + myAddressInfo[1]["publicKey"])
print("Your privateKey: " + myAddressInfo[1]["privateKey"])
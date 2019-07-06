from src import blockchain

bc = blockchain.Blockchain()

bc.append(blockchain.Block(
    data = [{
        "type": "data",
        "body": "Hello, world! This is the genesis block."
    }],
    previousHash = "0" * 64,
    address = "0" * 10
))

print(bc.blocks, bc.blocks[-1].data, bc.blocks[-1].hash)

myAddressInfo = blockchain.newAddress(bc.blocks[-1].hash)

bc.append(myAddressInfo[0])

print(bc.blocks, bc.blocks[-1].data, bc.blocks[-1].hash)

bc.verify(True)
from src import blockchain

bc = blockchain.Blockchain()

bc.append(blockchain.Block(
    data = [{
        "type": "data",
        "body": "Hello, world! This is the genesis block."
    }],
    previousHash = "0" * 64,
    address = ""
))

print(bc.blocks, bc.blocks[-1].data, bc.blocks[-1].hash)
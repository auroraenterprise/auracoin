import urllib
import urllib.request
import json
import shutil
import os

from src import blockchain, storage, server, networking, transactions

PEER_CHECK_FREQUENCY = 16
SAVE_FREQUENCY = 4
VERIFY_FREQUENCY = 4

def getBestPeerBlockchain():
    try:
        if server.verbose: print("- Downloading latest blockchain...")

        finalBlockchain = networking.nodeBlockchain
        highestDifficultySum = 0

        peerListURL = storage.getConfigItem("Peers", "peerList")
        peerListConnector = urllib.request.urlopen(peerListURL)
        peerList = peerListConnector.read().decode("utf-8").split("\n")
        finalPeers = []

        peerListConnector.close()

        for peer in peerList:
            if peer.startswith(";") or peer == "":
                pass
            else:
                finalPeers.append(peer)
        
        for peer in finalPeers:
            if server.verbose: print("- Checking peer blockchain " + peer + "...")

            peerConnector = urllib.request.urlopen(peer + "/getBlockchain")
            peerBlockchainData = json.loads(peerConnector.read().decode("utf-8"))

            peerConnector.close()

            peerBlockchain = blockchain.Blockchain()
            blocks = []

            for block in peerBlockchainData["blocks"]:
                newData = []

                for item in block["data"]:
                    if item["type"] == "transaction":
                        newTransaction = transactions.Transaction(
                            sender = item["body"]["sender"],
                            senderPublicKey = item["body"]["senderPublicKey"],
                            receiver = item["body"]["receiver"],
                            amount = item["body"]["amount"],
                            certificate = item["body"]["certificate"],
                            signature = item["body"]["signature"],
                            nonce = item["body"]["nonce"]
                        )

                        newData.append({
                            "type": item["type"],
                            "body": newTransaction,
                        })
                    else:
                        newData.append({
                            "type": item["type"],
                            "body": item["body"],
                        })
                
                newBlock = blockchain.Block(
                    data = newData,
                    previousHash = block["previousHash"],
                    address = "",
                    difficulty = block["difficulty"],
                    mine = False
                )

                newBlock.timestamp = block["timestamp"]
                newBlock.nonce = block["nonce"]
                newBlock.hash = block["hash"]

                blocks.append(newBlock)
            
            peerBlockchain.blocks = blocks
            peerBlockchain.difficulty = peerBlockchainData["difficulty"]

            dataString = ""

            for item in peerBlockchain.blocks[1].data:
                dataString += item["type"] + str(item["body"])
            
            if (
                peerBlockchain.__init__.__code__ == blockchain.Blockchain.__init__.__code__ and
                peerBlockchain.append.__code__ == blockchain.Blockchain.append.__code__ and
                peerBlockchain.verify.__code__ == blockchain.Blockchain.verify.__code__
            ):
                try:
                    peerBlockchain.verify(server.verbose)

                    if server.verbose: print("- Accepted peer blockchain, counting difficulty...")

                    difficultySum = 0

                    for block in peerBlockchain.blocks:
                        difficultySum += block.difficulty
                    
                    if difficultySum > highestDifficultySum:
                        highestDifficultySum = difficultySum

                        finalBlockchain = peerBlockchain
                except Exception as e:
                    if server.verbose: print("- Rejected peer blockchain: " + str(e))
        
        if server.verbose: print("- Best blockchain found")

        networking.nodeBlockchain = finalBlockchain
    except:
        if server.verbose: print("- Failed to download latest blockchain, maybe check settings or network connection")

def start():
    if server.verbose: print("- Miner started")

    try:
        networking.nodeBlockchain = storage.openObject("blockchain")

        getBestPeerBlockchain()
    except:
        getBestPeerBlockchain()

    currentCount = 0

    while True:
        if server.verbose: print("- Mining block...")

        networking.nodeBlockchain.append(blockchain.Block(
            data = networking.nodeRequests,
            previousHash = networking.nodeBlockchain.blocks[-1].hash,
            address = storage.getConfigItem("Account", "address"),
            difficulty = networking.nodeBlockchain.difficulty
        ))

        networking.nodeRequests = []

        if server.verbose: print("- Mined block, block reward A." + str(transactions.BLOCK_REWARD) + " sent to " + storage.getConfigItem("Account", "address"))

        currentCount += 1

        if currentCount % PEER_CHECK_FREQUENCY == 0:
            getBestPeerBlockchain()
        
        if currentCount % SAVE_FREQUENCY == 0:
            if server.verbose: print("- Saving blockchain to file...")

            try:
                shutil.copyfile(os.path.join(storage.CONFIG_FOLDER, "blockchain.auo"), os.path.join(storage.CONFIG_FOLDER, "blockchain.auo.old"))
            except: pass

            storage.saveObject(networking.nodeBlockchain, "blockchain")

            try:
                os.remove(os.path.join(storage.CONFIG_FOLDER, "blockchain.auo.old"))
            except: pass

            if server.verbose: print("- Saved blockchain to file ~/.auracoin/blockchain.auo")
        
        if currentCount % VERIFY_FREQUENCY == 0:
            if server.verbose: print("- Verifying blockchain...")

            try:
                networking.nodeBlockchain.verify(server.verbose)

                if server.verbose: print("- Accepted blockchain")
            except Exception as e:
                if server.verbose: print("- Rejected blockchain: " + str(e))

                getBestPeerBlockchain()
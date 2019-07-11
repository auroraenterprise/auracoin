import urllib
import pickle
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
            peerBlockchain = pickle.load(peerConnector)

            peerConnector.close()

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

            shutil.copyfile(os.path.join(storage.CONFIG_FOLDER, "blockchain.auo"), os.path.join(storage.CONFIG_FOLDER, "blockchain.auo.old"))

            storage.saveObject(networking.nodeBlockchain, "blockchain")

            os.remove(os.path.join(storage.CONFIG_FOLDER, "blockchain.auo.old"))

            if server.verbose: print("- Saved blockchain to file ~/.auracoin/blockchain.auo")
        
        if currentCount % VERIFY_FREQUENCY == 0:
            if server.verbose: print("- Verifying blockchain...")

            try:
                networking.nodeBlockchain.verify(server.verbose)

                if server.verbose: print("- Accepted blockchain")
            except Exception as e:
                if server.verbose: print("- Rejected blockchain: " + str(e))

                getBestPeerBlockchain()
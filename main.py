import argparse
import shutil
import os
import sys

from src import blockchain, storage, transactions, server

cli = argparse.ArgumentParser(
    prog = "auracoin",
    description = "Aurora's new cryptocurrency integrated with Aurachain."
)

cli.add_argument("-v", "--verbose", help = "show verbose output when running")

arguments = cli.parse_args()

config = {}

try:
    config["address"] = storage.getConfigItem("Account", "address")
    config["publicKey"] = storage.getConfigItem("Account", "publicKey")
    config["privateKey"] = storage.getConfigItem("Account", "privateKey")

    assert len(config["address"]) == transactions.ADDRESS_LENGTH
    assert len(config["publicKey"]) == 128
    assert len(config["privateKey"]) == 64
except:
    print("Your configuration file at ~/.auracoin/config.auc is missing or not configured properly.")

    try:
        shutil.copytree("config", storage.CONFIG_FOLDER)

        print("It has been automatically added along with other files; please configure it in order to run headless.")
    except:
        print("Automatic creation failed, please create the file and any other needed files.")

    sys.exit(1)

server.serve()
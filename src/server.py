# Auracoin
# 
# Copyright (C) Aurora Enterprise. All Rights Reserved.
# 
# https://aur.xyz
# Licensed by the Aurora Open-Source Licence, which can be found at LICENCE.md.

import http.server
import socketserver
import urllib
import sys

from src import info, storage, networking

verbose = False

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        returnMessage = "Status/fail/command"
        contentType = "text/plain"

        path = self.path.split("?")[0]
        fullPath = self.path
        queries = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        if path == "/":
            address = storage.getConfigItem("Account", "address")

            returnMessage = "Auracoin/{}/{}".format(info.VERSION_NUMBER, address)
        elif path == "/getBlockchain":
            contentType = "raw"
            cutoff = None
            address = None

            try:
                if "cutoff" in queries:
                    cutoff = int(queries["cutoff"][0])
                
                if "address" in queries:
                    address = queries["address"][0]

                returnMessage = networking.getBlockchain(cutoff, address)
            except:
                returnMessage = "Status/fail/format"
        elif path == "/getBlockHeight":
            try:
                returnMessage = "Status/ok/" + str(len(networking.nodeBlockchain.blocks))
            except:
                returnMessage = "Status/fail/exist"
        elif path == "/handleData":
            if "data" in queries:
                returnMessage = networking.handleData(queries["data"][0])
            else:
                returnMessage = "Status/fail/format"
        elif path == "/handleTransaction":
            if all(key in queries for key in ("sender", "senderPublicKey", "receiver", "amount", "certificate", "signature", "nonce")):
                returnMessage = networking.handleTransaction(
                    sender = queries["sender"][0],
                    senderPublicKey = queries["senderPublicKey"][0],
                    receiver = queries["receiver"][0],
                    amount = int(queries["amount"][0]),
                    certificate = queries["certificate"][0],
                    signature = queries["signature"][0],
                    nonce = int(queries["nonce"][0]),
                    verbose = verbose
                )
            else:
                returnMessage = "Status/fail/format"
        elif path == "/getAddressPublicKey":
            if "address" in queries:
                publicKey = networking.checkAddress(queries["address"][0])

                if publicKey == None:
                    returnMessage = "Status/fail/exist"
                else:
                    returnMessage = "Status/ok/" + publicKey
            else:
                returnMessage = "Status/fail/format"
        elif path == "/getAddressBalance":
            if "address" in queries:
                balance = networking.checkBalance(queries["address"][0])

                returnMessage = "Status/ok/" + str(balance)
            else:
                returnMessage = "Status/fail/format"
        elif path == "/handleRegistration":
            returnMessage = networking.handleRegistration()
        elif path == "/handleRegistrationFromPublicKey":
            if "publicKey" in queries:
                returnMessage = networking.handleRegistrationFromPublicKey(queries["publicKey"][0])
            else:
                returnMessage = "Status/fail/format"
        
        self.send_response(200)
        self.send_header("Content-type", contentType)
        self.end_headers()

        if isinstance(returnMessage, str):
            self.wfile.write(returnMessage.encode("utf-8"))
        else:
            self.wfile.write(returnMessage)
    
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        http.server.BaseHTTPRequestHandler.end_headers(self)

def serve():
    socketserver.TCPServer.allow_reuse_address = True

    try:
        httpSocket = socketserver.TCPServer((storage.getConfigItem("Peers", "outboundIP"), int(storage.getConfigItem("Peers", "outboundPort"))), Handler)
    except:
        print("Could not start server at {}:{}. Check if IP address and port is usable and free.".format(storage.getConfigItem("Peers", "outboundIP"), storage.getConfigItem("Peers", "outboundPort")))
        sys.exit(1)

    if verbose: print("- Serving port {}:{}...".format(storage.getConfigItem("Peers", "outboundIP"), storage.getConfigItem("Peers", "outboundPort")))

    try:
        httpSocket.serve_forever()
    except:
        httpSocket.shutdown()
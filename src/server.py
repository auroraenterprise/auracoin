import http.server
import socketserver
import urllib

from src import info, storage, networking

verbose = False

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        returnMessage = ""
        contentType = "text/plain"

        path = self.path.split("?")[0]
        fullPath = self.path
        queries = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        if path == "/":
            address = storage.getConfigItem("Account", "address")

            returnMessage = "Auracoin/{}/{}".format(info.VERSION_NUMBER, address)
        elif path == "/getBlockchain":
            contentType = "raw"

            returnMessage = networking.getBlockchain()
        elif path == "/handleData":
            if "data" in queries:
                returnMessage = networking.handleData(queries["data"])
            else:
                returnMessage = "Status/fail/format"
        elif path == "/handleTransaction":
            if all(key in queries for key in ("sender", "senderPublicKey", "receiver", "amount", "certificate", "signature", "nonce")):
                returnMessage = networking.handleData(
                    sender = queries["sender"],
                    senderPublicKey = queries["senderPublicKey"],
                    receiver = queries["receiver"],
                    amount = queries["amount"],
                    certificate = queries["certificate"],
                    signature = queries["signature"],
                    nonce = queries["nonce"],
                    verbose = verbose
                )
            else:
                returnMessage = "Status/fail/format"
        elif path == "/handleRegistration":
            returnMessage = networking.handleRegistration()
        
        self.send_response(200)
        self.send_header("Content-type", contentType)
        self.end_headers()

        if isinstance(returnMessage, str):
            self.wfile.write(returnMessage.encode("utf-8"))
        else:
            self.wfile.write(returnMessage)

def serve():
    socketserver.TCPServer.allow_reuse_address = True
    httpSocket = socketserver.TCPServer(("", 5000), Handler)

    try:
        httpSocket.serve_forever()
    except:
        httpSocket.shutdown()
import ecdsa
import base64
import hashlib
import random

from src.base40 import Base40

COINBASE_ADDRESS = "0" * 10
COINBASE_PUBLIC_KEY = "12ce3d4f9c137d337d5c07972ac99caa3ecc08aff96d876d702d9e31ae8a37e27dd9498591bd3d9ce62f71cc7164c6f51059395c89c8703a7fb9826348b0ee1e"
COINBASE_PRIVATE_KEY = "ae81085a32fe78b53cee28dd9fd325e8045c78e9b73906a5bfc1590c70b1ce57"

BLOCK_REWARD = 10 ** 8
ADDRESS_LENGTH = 10
TRANSACTION_NONCE_RANGE = (2 ** 64) - 1

class Transaction:
    def __init__(self, sender, senderPublicKey, receiver, amount, certificate, signature, nonce):
        assert len(sender) == ADDRESS_LENGTH
        assert len(senderPublicKey) == 128
        assert len(receiver) == ADDRESS_LENGTH
        assert amount > 0

        self.sender = sender
        self.receiver = receiver
        self.senderPublicKey = senderPublicKey
        self.amount = amount
        self.certificate = certificate
        self.signature = signature
        self.nonce = nonce

    def getCertificate(self):
        return str(self.sender) + str(self.senderPublicKey) + str(self.receiver) + str(self.amount) + str(self.nonce)

    def verify(self):
        if self.certificate == self.getCertificate():
            try:
                verifyingKey = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.senderPublicKey), curve = ecdsa.SECP256k1)

                return verifyingKey.verify(bytes.fromhex(self.signature), self.certificate.encode("utf-8"))
            except ecdsa.keys.BadSignatureError:
                return False
        else:
            return False

def newAddress():
    signingKey = ecdsa.SigningKey.generate(curve = ecdsa.SECP256k1)
    verifyingKey = signingKey.get_verifying_key()

    publicKey = bytes.hex(signingKey.to_string())
    privateKey = bytes.hex(verifyingKey.to_string())

    address = Base40().encode(int(hashlib.sha256(publicKey.encode("utf-8")).hexdigest(), 16))[:ADDRESS_LENGTH]

    return {
        "publicKey": publicKey,
        "privateKey": privateKey,
        "address": address
    }

def newReward(receiver):
    signingKey = ecdsa.SigningKey.from_string(bytes.fromhex(COINBASE_PRIVATE_KEY), curve = ecdsa.SECP256k1)
    certificate = str(COINBASE_ADDRESS) + str(COINBASE_PUBLIC_KEY) + str(receiver) + str(BLOCK_REWARD)
    signature = bytes.hex(signingKey.sign(certificate.encode("utf-8")))

    return Transaction(COINBASE_ADDRESS, COINBASE_PUBLIC_KEY, receiver, BLOCK_REWARD, certificate, signature, random.randint(0, TRANSACTION_NONCE_RANGE))
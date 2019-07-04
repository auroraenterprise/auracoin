import ecdsa
import base64

COINBASE_PUBLIC_KEY = "12ce3d4f9c137d337d5c07972ac99caa3ecc08aff96d876d702d9e31ae8a37e27dd9498591bd3d9ce62f71cc7164c6f51059395c89c8703a7fb9826348b0ee1e"
COINBASE_PRIVATE_KEY = "ae81085a32fe78b53cee28dd9fd325e8045c78e9b73906a5bfc1590c70b1ce57"

BLOCK_REWARD = 10 ** 8

class Transaction:
    def __init__(self, sender, receiver, amount, certificate, signature):
        assert len(sender) == 128
        assert len(receiver) == 128
        assert amount > 0

        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.certificate = certificate
        self.signature = signature

    def getCertificate(self):
        return str(self.sender) + str(self.receiver) + str(self.amount)

    def verify(self):
        if self.certificate == self.getCertificate():
            try:
                verifyingKey = ecdsa.VerifyingKey.from_string(bytes.fromhex(self.sender), curve = ecdsa.SECP256k1)

                return verifyingKey.verify(bytes.fromhex(self.signature), self.certificate.encode("utf-8"))
            except ecdsa.keys.BadSignatureError:
                return False
        else:
            return False

def newReward(receiver):
    signingKey = ecdsa.SigningKey.from_string(bytes.fromhex(COINBASE_PRIVATE_KEY), curve = ecdsa.SECP256k1)
    certificate = str(COINBASE_PUBLIC_KEY) + str(receiver) + str(BLOCK_REWARD)
    signature = bytes.hex(signingKey.sign(certificate.encode("utf-8")))

    return Transaction(COINBASE_PUBLIC_KEY, receiver, BLOCK_REWARD, certificate, signature)
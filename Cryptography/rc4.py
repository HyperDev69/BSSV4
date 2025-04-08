import json
from Cryptography.RC4Encrypter import RC4Encrypter as RC4

cyan = "\033[36m"

class CryptoRc4:
    def __init__(self):
        self.settings = json.load(open('Settings.json'))
        self.key = bytes(self.settings["RC4Key"], 'utf-8')
        # print(cyan + f"[PLAYER] New connection! RC4 key:{self.key}")
        self.nonce = b'nonce'
        self.RC4_Stream = RC4(self.key + self.nonce)
        self.RC4_Stream.update(self.key + self.nonce)
        self.RC4_Stream2 = RC4(self.key + self.nonce)
        self.RC4_Stream2.update(self.key + self.nonce)

    def decrypt(self, data):
        return self.RC4_Stream.update(data)

    def encrypt(self, data):
        return self.RC4_Stream2.update(data)

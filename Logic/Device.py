import json
from Cryptography.rc4 import CryptoRc4
from Packets.Factory import *

red = "\033[31m"

class Device:

    AndroidID = None
    DeviceModel = None
    OpenUDID = None
    OSVersion = None
    IsAndroid = False

    Player = None

    players = 0
    ClientDict = {}

    def __init__(self, socket=None):
        self.socket = socket
        self.crypto = CryptoRc4()
        with open('Settings.json') as f:
            self.settings = json.load(f)
        self.usedCryptography = self.settings["usedCryptography"]

    def SendData(self, ID, data, version=None):
        encrypted = self.crypto.encrypt(data)

        packetID = ID.to_bytes(2, 'big')

        if version:
            packetVersion = version.to_bytes(2, 'big')
        else:
            packetVersion = (0).to_bytes(2, 'big')

        if self.socket:
            self.socket.send(packetID + len(encrypted).to_bytes(3, 'big') + packetVersion + encrypted)
        else:
            self.transport.write(packetID + len(encrypted).to_bytes(3, 'big') + packetVersion + encrypted)

    def SendDataTo(self, ID, data, target, version=None):
        encrypted = self.crypto.encrypt(data)

        packetID = ID.to_bytes(2, 'big')
        packetVersion = (version if version else 0).to_bytes(2, 'big')

        if str(target) not in self.ClientDict.get("Clients", {}):
            print(red + f"[ERROR] Target {target} not found!")
            return

        PlayerSocket = self.ClientDict["Clients"][str(target)]["SocketInfo"]



    def decrypt(self, data):
        return self.crypto.decrypt(data)

    def processPacket(self, packetID, payload):

        print(red + f'[INFO] {packetID} received')

        try:
            decrypted = self.decrypt(payload)

            if packetID in availablePackets:
                Message = availablePackets[packetID](decrypted, self)
                Message.decode()
                Message.process()
        except Exception as e:
            print(red + f"[ERROR] {e}")

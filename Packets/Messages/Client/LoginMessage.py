from Utils.Reader import ByteStream
from Packets.Messages.Server.LoginOkMessage import LoginOkMessage
from Packets.Messages.Server.LoginFailedMessage import LoginFailedMessage
from Packets.Messages.Server.OwnHomeDataMessage import OwnHomeDataMessage
from Logic.Player import Player
from Packets.Messages.Server.ClanData import ClanData
from Packets.Messages.Server.ClanStream import ClanStream
import time
import json

class LoginMessage(ByteStream):
    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player  
        
    # Login infos start
    def decode(self):
        self.settings = json.load(open('Settings.json'))
        self.isInMaintenance = self.settings["isInMaintenance"]
        isInMaintenance = self.isInMaintenance
        self.loginPayload = {}
        self.loginPayload["highID"] = self.readInt()
        self.loginPayload["lowID"] = self.readInt()
        self.loginPayload["token"] = self.readString()
        self.loginPayload["majorVersion"] = self.readInt()
        self.loginPayload["minorVersion"] = self.readInt()
        self.loginPayload["build"] = self.readInt()
        self.loginPayload["fingerprintSHA"] = self.readString()
        self.loginPayload["unknown"] = self.readString()
        self.loginPayload["deviceID"] = self.readString()
        self.loginPayload["unknown1"] = self.readString()
        self.loginPayload["device"] = self.readString()
        self.loginPayload["systemLanguage"] = self.readVInt()
        self.loginPayload["region"] = self.readString().split('-')[1]
        self.player.usedVersion = self.loginPayload["majorVersion"]

    def process(self):
        if self.player.usedVersion == 4:
            if self.loginPayload["token"] == b'':
                self.loginPayload["token"] = "token"
            else:
                self.player.token = self.loginPayload["token"]
            
            self.player.high_id = self.loginPayload["highID"]
            self.player.low_id = self.loginPayload["lowID"]
            self.player.token = self.loginPayload["token"]
            self.player.region = self.loginPayload["region"]

            # Sending messages
            LoginOkMessage(self.device, self.player, self.loginPayload).Send()
            OwnHomeDataMessage(self.device, self.player).Send()
            ClanData(self.device, self.player).Send()
            ClanStream(self.device, self.player).Send()
        if self.player.isInMaintenance:
            LoginFailedMessage(self.device, self.player, self.loginPayload, "Server currently under maintenance, try later!", 10).Send()

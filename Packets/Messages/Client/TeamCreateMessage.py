from Packets.Messages.Server.TeamMessage import TeamMessage
import random
from Logic.Player import Player
from Utils.Reader import ByteStream

class TeamCreateMessage(ByteStream):
    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player
        
    def decode(self):
        pass

    def process(self):
        TeamMessage(self.device, self.player).Send()

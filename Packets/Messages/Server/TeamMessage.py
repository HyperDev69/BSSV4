from Utils.Writer import Writer
import random
import json
from Files.CsvLogic.Cards import Cards
from Files.CsvLogic.Characters import Characters

class TeamMessage(Writer):
    def __init__(self, device, player):
        self.id = 24124
        self.device = device
        self.player = player
        super().__init__(self.device)


    def encode(self):
            self.settings = json.load(open('Settings.json'))
            self.gameroom_brawler = self.settings["gameroom_brawler"]
            self.name = self.settings["name"]
            self.BrawlerTrophies = self.settings["BrawlerTrophies"]
            self.BrawlerTrophies_perRank = self.settings["BrawlerTrophies_perRank"]
            self.gameroom_status = self.settings["gameroom_status"]
            
            self.writeVInt(0) # Unknown
            self.writeBoolean(False) # Pratice aganist bots
            self.writeVInt(0) # Unknown
            self.writeLong(0, 0) # Player's highID and lowID (?)
            self.writeVInt(0) # Unknown
            self.writeVInt(0) # Unknown
            self.writeVInt(0) # Unknown
            self.writeScID(15, 5) # Map
            self.writeVInt(1) # Players count
            for player in range(1):
                
                if player == 0:
                    self.writeLong(0, self.player.low_id) # Player ID
                    
                self.writeString(self.name) # Player Name
                self.writeVInt(0) # Unknown
                self.writeScID(self.gameroom_brawler[0], self.gameroom_brawler[1]) # Brawler
                self.writeScID(29, 0) # Unknown
                self.writeVInt(self.BrawlerTrophies) # Brawler Trophies
                self.writeVInt(self.BrawlerTrophies_perRank) # Brawler Trophies for Rank
                self.writeVInt(0) # Power level 

from Logic.Milestones import Milestones
from Logic.Player import Player
from Utils.Writer import Writer
import random
from Files.CsvLogic.Cards import Cards
from Files.CsvLogic.Characters import Characters
from Files.CsvLogic.Locations import Locations
import json
from datetime import datetime

class OwnHomeDataMessage(Writer):

    def __init__(self, device, player):
        self.id = 24101
        self.device = device
        self.player = player
        super().__init__(self.device)

    def encode(self):
        self.settings = json.load(open('Settings.json'))
        self.maximumRank = self.settings["MaximumRank"]
        self.tutorial_state = self.settings["tutorial_state"]
        self.BrawlerTrophies = self.settings["BrawlerTrophies"]
        self.BrawlerTrophies_perRank = self.settings["BrawlerTrophies_perRank"]
        self.gems = self.settings["gems"]
        self.gold = self.settings["gold"]
        self.chips = self.settings["chips"]
        self.elixir = self.settings["elixir"]
        self.Experience = self.settings["ExperiencePoints"]
        self.ControlMode = self.settings["ControlMode"]
        self.trophies = self.settings["trophies"]
        self.coins_doubler = self.settings["coins_doubler"]
        self.coins_boost = self.settings["coins_boost"]
        self.Coins_to_Win = self.settings["Coins_to_Win"]
        self.HighestTrophies = self.settings["HighestTrophies"]
        self.events_timer = self.settings["events_timer"]
        self.events_coins_collected = self.settings["events_coins_collected"]
        self.events_type = self.settings["events_type"]
        self.player_icon = self.settings["player_icon"]
        self.coins_got = self.settings["coins_got"]
        self.name = self.settings["name"]
        self.events_count = self.settings["events_count"]
        self.events_bonusCoins = self.settings["events_bonusCoins"]

        cards = Cards().getCards()
        ressources_ids = [1, 5, 6]
        ressources = [self.gold, self.chips, self.elixir]

        self.writeVInt(2017189) # Timestamp
        self.writeVInt(10) # Create new band timer
        
        self.writeVInt(self.trophies)  # Trophies
        self.writeVInt(self.HighestTrophies)  # Highest Trophies
        self.writeVInt(self.Experience) # Experience
        self.writeVInt(0)
        
        self.writeScID(28, self.player_icon)  # Player Icon
        self.writeVInt(7) # Played Game Modes Count
        for x in range(7): 
            self.writeVInt(x) # Played Game Mode
        non_zero_skins = []
        for brawler in self.player.unlocked_brawlers.values():
            if brawler["selectedSkin"] != 0:
                non_zero_skins.append(brawler["selectedSkin"])
        self.writeVInt(len(non_zero_skins))
        for skin in non_zero_skins:
            self.writeDataReference(29, skin)
        
        non_zero_skins = []
        for brawler in self.player.unlocked_brawlers.values():
            for skin in brawler["Skins"]:
                if skin != 0:
                    non_zero_skins.append(skin)
        self.writeVInt(len(non_zero_skins))
        for skin in non_zero_skins:
            self.writeDataReference(29, skin)
        
        self.writeBool(False) # is time required to create new Band
        self.writeVInt(0) # unknown
        self.writeVInt(self.coins_got) # coins got
        self.writeBool(False)
        self.writeVInt(self.ControlMode) # Control Mode
        self.writeBool(False) # is battle hints enabled
        self.writeVInt(self.coins_doubler) # coins doubler
        self.writeVInt(self.coins_boost) # coin boost secs remaining
        self.writeVInt(0)
        self.writeBool(False)
        self.writeLogicLong(0, 1)

        self.writeLogicLong(0, 1)
        self.writeLogicLong(0, 1)
        self.writeLogicLong(0, 1)
        self.writeDataReference(0, 2)
        self.writeVInt(0)
        self.writeBoolean(True)
        self.writeBoolean(True)
        self.writeVInt(0)  # Shop Timestamp
        self.writeVInt(100) # box cost (gold)
        self.writeVInt(10) # box cost (gems)
        self.writeVInt(80) # box cost (gems)
        self.writeVInt(10) # box cost (gems)
        self.writeVInt(20) # Coin Boost cost
        self.writeVInt(50) # Coin Boost %
        self.writeVInt(50) # Coin Doubler cost
        self.writeVInt(50) # Coin Doubled
        self.writeVInt(24) # Coin Boost Hours
        self.writeVInt(500) # Minimum Brawler Trophies For Season Reset
        self.writeVInt(0) # Brawler Trophy Loss Percentage in Season Reset
        self.writeVInt(0) # Coin Limit Remaining
        self.writeArrayVInt([1,2,5,10,20,60])
        self.writeArrayVInt([3,10,20,60,200,500])
        self.writeArrayVInt([0,30,80,170,0,0])
        # Events array starts

        # Brawlers required for events starts

        self.writeVInt(self.events_count) # count

        requiredBrawlers = [0, 0, 0, 0] # all events unlocked

        for event in range(self.events_count):
            self.writeVInt(event + 1) # event index
            self.writeVInt(requiredBrawlers[event]) # Brawlers needed for that

        # Brawlers required for events ends
        
        # disponible events starts
        
        self.writeVInt(self.events_count) # disponibles event slot
        for events in range(self.events_count):
            self.writeVInt(events + 0) # slot index
            self.writeVInt(events + 0) # slot number
            self.writeVInt(self.events_timer) # comming soon timer
            self.writeVInt(self.events_timer) # Time Left
            self.writeVInt(self.events_bonusCoins) # coins to claim
            self.writeVInt(self.events_bonusCoins) # bonuska coins
            self.writeVInt(self.Coins_to_Win) # coins to win
            self.writeBoolean(False) # double coins
            self.writeBoolean(False) # double exp
            self.writeScID(15, random.randint(0, 20)) # map
            self.writeVInt(self.events_coins_collected) #  coins already collected
            self.writeVInt(self.events_type) #  related to free coins rewards
            self.writeString() # lobby info
            self.writeBoolean(False)

        # disponible events ends
        
        # comming soon events starts
        self.writeVInt(4) # disponibles event slot
        for events in range(4):
            self.writeVInt(events+1) # slot index
            self.writeVInt(events+1) # slot number
            self.writeVInt(self.events_timer) # coming soon timer
            self.writeVInt(self.events_timer) # Time Left
            self.writeVInt(self.events_bonusCoins) # coins to claim
            self.writeVInt(self.events_bonusCoins) # bonuska coins
            self.writeVInt(self.Coins_to_Win) # coins to win
            #self.writeVInt(2) # event type , 1= double coins (??) 2+ = double xp 3 = double coins + exp
            self.writeBoolean(False) # double coins
            self.writeBoolean(False) # double exp
            self.writeScID(15, 0) # map
            self.writeVInt(self.events_coins_collected) #  coins already collected
            self.writeVInt(self.events_type) #  coins collected statut
            self.writeString("<cff0e00>h<cff1c00>t<cff2a00>t<cff3800>p<cff4600>s<cff5500>:<cff6300>/<cff7100>/<cff7f00>g<cff8d00>i<cff9b00>t<cffaa00>h<cffb800>u<cffc600>b<cffd400>.<cffe200>c<cfff000>o<cfeff00>m<cffff00>/<cf0ff00>H<ce2ff00>y<cd4ff00>p<cc6ff00>e<cb8ff00>r<ca9ff00>D<c9bff00>e<c8dff00>v<c7fff00>6<c71ff00>9<c63ff00>/<c54ff00>B<c46ff00>S<c38ff00>S<c2aff00>V<c1cff00>4</c>") # lobbyinfo
            self.writeBoolean(False)
        # comming soon event ends
            
        # Events array ends
        
        self.writeVInt(0) # upgrades Array
        for x in range(0):
            self.writeVInt(1) # price
        
        Milestones.MilestonesArray(self)
        
        
        self.writeLong(self.player.high_id, self.player.low_id)  # Player id
        self.writeVInt(0)
        for id in range(3):
            self.writeLogicLong(self.player.high_id, self.player.low_id) # Player ids related to menu
        
        self.writeString(self.name)
        self.writeBool(self.name != "Brawler") # nameSet (useless)
        self.writeInt(1)
        
        # motorised arrays stars 
        self.writeVInt(5) # Array
        cards = {}
        for key, brawler in self.player.unlocked_brawlers.items():
            for card, amount in brawler["Cards"].items():
                cards[card] = amount
        self.writeVInt(len(cards) + len(ressources_ids)) # cards and ressources array
        for key, amount in cards.items():
            self.writeScId(23, int(key))
            self.writeVInt(amount) # upgrades count
        
        # ressources
        for res in range(len(ressources_ids)):
            self.writeScID(5, ressources_ids[res]) # resource 
            self.writeVInt(ressources[res]) # count
            
        # cards and ressources Array End
        
        self.writeVInt(len(self.player.unlocked_brawlers))  # brawlers count
        for key, brawler_id in self.player.unlocked_brawlers.items():
            self.writeDataReference(16, int(key))
            self.writeVInt(self.BrawlerTrophies)

        # Brawlers Trophies for Rank array
        self.writeVInt(len(self.player.unlocked_brawlers))  # brawlers count
        for key, brawler_id in self.player.unlocked_brawlers.items():
            self.writeDataReference(16, int(key))
            self.writeVInt(self.BrawlerTrophies_perRank)
        
        self.writeVInt(0)
        # brawler seen state array
        self.writeVInt(len(self.player.unlocked_brawlers))  # brawlers count
        for key, brawler_id in self.player.unlocked_brawlers.items():
            self.writeDataReference(16, int(key))
            self.writeVInt(2)
        
        self.writeVInt(self.gems) # gems
        self.writeVInt(0)
        
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        self.writeVInt(0)
        
        self.writeVInt(self.tutorial_state)
        self.writeVInt(2017189)

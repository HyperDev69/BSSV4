from Utils.Writer import Writer
import json

class ClanData(Writer):
           def __init__(self, device, player):
               self.id = 24399
               self.device = device
               self.player = player
               super().__init__(self.device)

           def encode(self):
               isInClub = True
               self.settings = json.load(open('Settings.json'))
               self.club_name = self.settings["club_name"]
               self.club_trophies = self.settings["club_trophies"]
               self.club_members = self.settings["club_members"]
               self.club_icon = self.settings["club_icon"]
               if isInClub:
                      self.writeVInt(0) # High ID
                      self.writeVInt(1) # Low ID
			
                      self.writeScID(0, 0) # Role?
                      self.writeInt(0) # Unknown
                      self.writeInt(0) # Unknown
                      self.writeString(self.club_name) # Club Name
                      self.writeScID(8, self.club_icon) # Club Icon
                      self.writeVInt(0) # Unknown
                      self.writeVInt(self.club_members) # Members
                      self.writeVInt(self.club_trophies) # Trophies

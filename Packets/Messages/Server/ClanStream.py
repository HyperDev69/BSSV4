from Utils.Writer import Writer

class ClanStream(Writer):
    def __init__(self, device, player):
         self.id = 24311
         self.device = device
         self.player = player
         super().__init__(self.device)

    def encode(self):
        data = "04-00-82-D5-84-03-01-80-24-00-00-00-08-68-79-70-65-72-64-65-76-01-BD-D9-0F-00-03-00-04-00-86-8D-98-03-00-84-E6-01-00-00-00-06-54-6F-6A-6F-6B-6F-02-BA-A3-0A-00-05-01-01-80-24-00-00-00-08-68-79-70-65-72-64-65-76-04-00-87-8D-98-03-00-84-E6-01-00-00-00-06-54-6F-6A-6F-6B-6F-02-BA-A3-0A-00-04-00" # Hex dump from Berkan
        self.writeVInt(3)
        self.writeHexa(data, len(data))

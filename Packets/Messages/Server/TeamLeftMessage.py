from Utils.Writer import Writer

class TeamLeftMessage(Writer):

    def __init__(self, device, player):
        self.id = 24125
        self.device = device
        self.player = player
        super().__init__(self.device)

    def encode(self):
        self.writeVInt(0) # Exit message (0 = you left the room 1 = you were kicked from the room 2 = the room has been discarded)

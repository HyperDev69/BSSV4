from Packets.Messages.Server.OwnHomeDataMessage import OwnHomeDataMessage
from Utils.Reader import ByteStream


class GoHomeFromOfflineMessage(ByteStream):

    def __init__(self, data, device, player):
        super().__init__(data)
        self.id = 14109
        self.device = device
        self.data = data
        self.player = player

    def decode(self):
        None

    def process(self):
        OwnHomeDataMessage(self.device, self.player).Send()

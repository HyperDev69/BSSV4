from Utils.Writer import Writer
from Utils.Fingerprint import Fingerprint
import json

"""Login Failed Codes (Write when sending)
    
   1. Login Failed
   8. Update available 
   10. Maintenance break
   12. Personal break TID
   16. Version not up to date shop not ready TID

"""

class LoginFailedMessage(Writer):

    def __init__(self, device, player, loginPayload, msg , errorCode):
        super().__init__(device)
        self.id = 20103
        self.device = device
        self.player = player
        self.loginPayload = loginPayload
        self.msg = msg
        self.errorCode = errorCode

    def encode(self):
        self.settings = json.load(open('Settings.json'))
        self.UpdateUrl = self.settings["UpdateUrl"]
        
        self.writeInt(self.errorCode)

        self.writeString(self.loginPayload["fingerprintSHA"])

        self.writeString("0.0.0.0:9339")

        self.writeString("")
        self.writeString(self.UpdateUrl)
        self.writeString(self.msg)

        self.writeVInt(0)
        self.writeBoolean(False)

        self.writeString()
        self.writeString()

        self.writeInt(0)
        self.writeInt(3)

        self.writeInt(0)
        self.writeInt(0)

        self.writeBoolean(False)
        self.writeBoolean(False)

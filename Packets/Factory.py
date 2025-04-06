from Packets.Messages.Client import *


availablePackets = {
    10100: ClientHelloMessage,
    10101: LoginMessage,
    10108: KeepAliveMessage,
    14109: GoHomeFromOfflineMessage,
    14350: TeamCreateMessage,
    14353: TeamLeaveMessage
}

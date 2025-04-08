import socket
import json
import traceback
from threading import Thread, Lock
from Packets.Factory import *
from Logic.Device import Device
from Packets.Messages.Server.LobbyInfoMessage import LobbyInfoMessage
from Logic.Player import Player

connected_clients_count = 0
client_count_lock = Lock()
# Colors
red = "\033[31m"
blue = "\033[34m"
yellow = "\033[33m"

class Networking(Thread):
    Clients = {"ClientCounts": 0, "Clients": {}}

    def __init__(self):
        Thread.__init__(self)
        
        with open('Settings.json') as f:
            self.settings = json.load(f)
        
        self.usedCryptography = self.settings["usedCryptography"]
        self.address = self.settings["Address"]
        self.port = self.settings["Port"]
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        global connected_clients_count
        self.server.bind((self.address, self.port))
        self.server.listen(5)

        while True:
            client, address = self.server.accept()

            with client_count_lock:
                connected_clients_count += 1
                print(yellow + f"[PLAYER] Players online: {connected_clients_count}")

            print(blue + f'[PLAYER] New connection from {address[0]}')
            clientThread = ClientThread(client, address)
            clientThread.start()


class ClientThread(Thread):
    def __init__(self, client, address):
        Thread.__init__(self)
        self.address = address
        self.client = client
        self.device = Device(self.client)
        self.player = Player(self.device)
        
        with open('Settings.json') as f:
            self.settings = json.load(f)
        
        self.usedCryptography = self.settings["usedCryptography"]

    def recvall(self, size):
        data = b''
        while size > 0:
            s = self.client.recv(size)
            if not s:
                print(red + "[ERROR] Disconnection from client.")
                raise EOFError
            data += s
            size -= len(s)
        return data

    def run(self):
        global connected_clients_count

        try:
            while True:
                header = self.client.recv(7)
                if len(header) < 7:
                    print(red + '[ERROR] Received an invalid packet from client/Player disconnected')
                    self.client.close()
                    break

                packetid = int.from_bytes(header[:2], 'big')
                length = int.from_bytes(header[2:5], 'big')
                version = int.from_bytes(header[5:], 'big')
                data = self.recvall(length)

                LobbyInfoMessage(self.device, self.player, connected_clients_count).Send()

                if length == len(data):
                    print(blue + f'[INFO] {packetid} received')

                    try:
                        if self.usedCryptography == "RC4":
                            decrypted = self.device.decrypt(data)
                        else:
                            decrypted = data

                        if packetid in availablePackets:
                            Message = availablePackets[packetid](decrypted, self.device, self.player)
                            Message.decode()
                            Message.process()

                            if packetid == 10101:
                                Networking.Clients["Clients"][str(self.player.low_id)] = {"SocketInfo": self.client}
                                Networking.Clients["ClientCounts"] = connected_clients_count
                                self.device.ClientDict = Networking.Clients
                    except Exception as e:
                        print(traceback.format_exc())
        
        finally:
            with client_count_lock:
                connected_clients_count -= 1
                try:
                    del Networking.Clients["Clients"][str(self.player.low_id)]
                except KeyError:
                    pass
                
                Networking.Clients["ClientCounts"] = connected_clients_count
                self.device.ClientDict = Networking.Clients

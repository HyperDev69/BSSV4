import os
import socket
import argparse

from threading import *
from Networking import *

red ='\033[91m'
green = '\033[92m'

print(red + f'[INFO] Starting server...')
print(red + f'[GITHUB] hyperdev69')
print(red + f'[TELEGRAM] @hyperd3v')
print("""
  ____   _____ _____ 
 |  _ \ / ____/ ____|
 | |_) | (___| (___  
 |  _ < \___ \\___  \ 
 | |_) |____) |___) |
 |____/|_____/_____/ 
                     
                                                  
""")
print(green + f'[INFO] Server started! Welcome to BSSV4')
Networking().start()

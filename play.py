import json
import os

# import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# set up bitrequest client for BitTransfer requests
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

# server address
server_url = 'http://localhost:5000/'

def play():

    # get the question from the server
    response = requests.get(url=server_url+'lotterMe')
    question = response.text
    print(question)

if __name__ == '__main__':
    play()
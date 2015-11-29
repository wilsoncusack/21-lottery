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
server_url = 'http://192.168.1.245:5000/' # need to change this to globally accessible address  

def play():

    lotter_url = server_url+'lotterMe?payout_address={0}'
    response = requests.get(url=lotter_url.format(wallet.get_payout_address()))
    print(response.text)

if __name__ == '__main__':
    play()
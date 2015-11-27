import os
import json
import random
import psycopg2

# import flask web microframework
from flask import Flask
from flask import request

# import from the 21 Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)


# machine-payable endpoint that pays user if answer is correct
@app.route('/lotterMe')
@payment.required(1000)
def placeBet():
    print("in route")
    betsTableConnection = psycopg2.connect(database="bets", user="twenty", password="md556eb55a1978f8a1a6a7149914d371379")
    betsTable = betsTableConnection.cursor()
    print("connected to bets table")
    roundsTableConnection = psycopg2.connect(database="bets", user="twenty", password="md556eb55a1978f8a1a6a7149914d371379")
    roundsTable = roundsTableConnection.cursor()
    print("connected to rounds table")
    winningBetNumber = roundsTable.execute("SELECT winvalue from rounds ORDER BY id DESC;")

    betCount = betsTable.execute("SELECT max(id) FROM bets;")

    if betCount + 1 == winningBetNumber:
        betsTable.execute("SELECT pot_size FROM lottery;")
        winningAddresss = request.args.get('payout_address')
        winningPotAmount = roundsTable.execute("SELECT win_size from rounds ORDER BY id DESC;")

        print("pot size = " + str(winningPotAmount))
        print(winningAddresss)

        print("did you get here?")
        txid = wallet.send_to(winningAddresss, winningPotAmount)
        print("got here")
        ########################
        # somehow calculate the new pot size
        # newPotSize = pot
        # roundSize = lastroundSize * 2
        # newWinningBetNumber = getWinningBetNumberFromRange()
        ######################
        betsTable.close()
        roundsTable.close()

        return "You win!"
    else:
        print("in else statement")
        betsTable.execute("INSERT INTO bets (addresss) VALUES (" + request.args.get('payout_address') + ");")

        betsTable.close()
        roundsTable.close()

        return "Sorry! Try again!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
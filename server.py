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
    dataBaseConnection = psycopg2.connect(database="lottery3", user="twenty", password="md556eb55a1978f8a1a6a7149914d371379")
    connection = dataBaseConnection.cursor()
    print("connected to DB")
    # betsTableConnection = psycopg2.connect(database="bets", user="twenty", password="md556eb55a1978f8a1a6a7149914d371379")
    # betsTable = betsTableConnection.cursor()
    # roundsTableConnection = psycopg2.connect(database="bets", user="twenty", password="md556eb55a1978f8a1a6a7149914d371379")
    # roundsTable = roundsTableConnection.cursor()

    winningBetNumber = connection.execute("SELECT winvalue from rounds ORDER BY id DESC;")
    print("first query")
    betCount = connection.execute("SELECT max(id) FROM bets;")
    print("second query")
    if betCount + 1 == winningBetNumber:
        print("in if")
        connection.execute("SELECT pot_size FROM lottery;")
        winningAddresss = request.args.get('payout_address')
        winningPotAmount = connection.execute("SELECT win_size from rounds ORDER BY id DESC;")

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
        connection.close()
        # roundsTable.close()

        return "You win!"
    else:
        print("in else statement")
        connection.execute("INSERT INTO bets (addresss) VALUES (" + request.args.get('payout_address') + ");")

        connection.close()
        # roundsTable.close()

        return "Sorry! Try again!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')

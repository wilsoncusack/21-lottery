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


# endpoint to get a question from the server
#@app.route('/lotterMe')

# machine-payable endpoint that pays user if answer is correct
@app.route('/lotterMe')
@payment.required(1000)
def answer_question():
    conn = psycopg2.connect(database="lottery3", user="twenty", password="md556eb55a1978f8a1a6a7149914d371379")
    cursor = conn.cursor()

    client_payout_addr = request.args.get('payout_address')
    cursor.execute("INSERT INTO bids (address) VALUES (%s);", (client_payout_addr,))
    print("here")
    client_bid_number = cursor.fetchone()[0]
    print(client_bid_number)

    cursor.execute("SELECT winning_bid_number FROM rounds ORDER BY round_number desc LIMIT 1;")
    winning_bid_number = cursor.fetchone()[0]

    if winning_bid_number == client_bid_number:
        cursor.execute("SELECT pot_size FROM lottery;")
        potSize = int(cursor.fetchone()[0])
        print("pot size = " + str(potSize))

        print(request.args.get('payout_address'))

        client_payout_addr = request.args.get('payout_address')
        print("did you get here?")
        #txid = wallet.send_to(client_payout_addr, potSize)
        print("got here")
        SQL = "UPDATE lottery SET pot_size = %s;"
        newPotSize = (potSize/2) + 3000
        data = (newPotSize,)
        cursor.execute(SQL, data)

        conn.commit()
        cursor.close() 

        return "You win!"
    else:
        conn.commit()
        cursor.close() 

        return "Sorry! Try again!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
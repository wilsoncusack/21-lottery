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
def update_count(newCount, cursor):
    print("in count!!")
    SQL = "UPDATE lottery SET request_count = %s;"
    data = (newCount,)
    cursor.execute(SQL, data)

# machine-payable endpoint that pays user if answer is correct
@app.route('/lotterMe')
@payment.required(1000)
def answer_question():
    conn = psycopg2.connect(database="lottery3", user="twenty", password="md556eb55a1978f8a1a6a7149914d371379")
    cursor = conn.cursor()

    cursor.execute("SELECT request_count FROM lottery;")
    count = cursor.fetchone()[0]
    print("count = " + str(count))

    #cursor.execute("SELECT request_count FROM lottery;")
    #iteration = cursor.fetchone()[0]

    if (count + 1) == 3:
        cursor.execute("SELECT pot_size FROM lottery;")
        potSize = cursor.fetchone()[0]
        print("pot size = " + str(potSize))
        print(request.args)
        print(request.args.get('payout_address'))

        client_payout_addr = request.args.get('payout_address')
        txid = wallet.send_to(client_payout_addr, potSize)
        print("got here")
        SQL = "UPDATE lottery SET pot_size = %s;"
        newPotSize = (potSize/2) + 3000
        data = (newPotSize,)
        cursor.execute(SQL, data)
        print("and here")
        update_count(0, cursor)

        conn.commit()
        cursor.close() 
        print("ended!")

        return "You win!"
    else:
        update_count((count + 1), cursor)

        conn.commit()
        cursor.close() 
        print("ended!") 

        return "Sorry! Try again!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
import os
import json
import random
import psycopg2
import math

# import flask web microframework
from flask import Flask
from flask import request
from flask import render_template

# import from the 21 Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)


# endpoint to get a question from the server
@app.route('/view')
@payment.required(0)
def view():
    conn = psycopg2.connect(database="lottery3", user="twenty", password="md556eb55a1978f8a1a6a7149914d371379")
    cursor = conn.cursor()
    # can just grab the data here
    cursor.execute("SELECT * FROM rounds ORDER BY round_number asc;") # need to modify to not return the most recent
    result = cursor.fetchall()
    print(result)
    length = len(result)
    data = [i for i in range(length)]
    for d in result:
        # rounds should start from zero in the future
        print('up here')
        data[d[0] - 1] = [d[0], d[1], d[2]]
        print('down here')
        #data[d[0] - 1] = dict(round_number = d[0], winning_bid_number = d[1], pot_size = d[2])
        #data[d[0] - 1] = flask.jsonify(**data[d[0] - 1])
        #data[d[0] - 1] = {"round_number": d[0], "winning_bid_number": d[1], "pot_size": d[2]}
    data[length - 1][1] = -1
    print(data)
    return render_template('index.html', data=data)

# machine-payable endpoint that pays user if answer is correct
@app.route('/lotterMe')
@payment.required(200)
def answer_question():
    conn = psycopg2.connect(database="lottery3", user="twenty", password="md556eb55a1978f8a1a6a7149914d371379")
    cursor = conn.cursor()

    client_payout_addr = request.args.get('payout_address')
    cursor.execute("INSERT INTO bids (address) VALUES (%s) RETURNING id;", (client_payout_addr,))
    client_bid_number = cursor.fetchone()[0]

    # grabbing all of these things at once to minimize the number of requests to the db
    cursor.execute("SELECT round_number, winning_bid_number, pot_size FROM rounds ORDER BY round_number desc LIMIT 1;")
    [current_round_number, winning_bid_number, pot_size] = cursor.fetchone()

    print(pot_size)

    if winning_bid_number == client_bid_number:
        #txid = wallet.send_to(client_payout_addr, pot_size/2)

        cursor.execute("UPDATE bids SET is_winner = TRUE WHERE id = %s;", (client_bid_number,))

        random_number = math.floor(random.random()*(10*(2**(current_round_number + 1)))) + 1
        new_pot_size = (pot_size/2) + (random_number * 1000)

        SQL = "INSERT INTO rounds (winning_bid_number, pot_size) VALUES (%s, %s);"
        data = (random_number, new_pot_size,)
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
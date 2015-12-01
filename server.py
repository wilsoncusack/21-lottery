import os
import json
import random
import psycopg2
import math
import sys
import urllib.parse
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


# machine-payable endpoint that pays user if they are the winning request number
@app.route('/lotterMe')
@payment.required(200)
def lottery():
    urllib.parse.uses_netloc.append("postgres")
    url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cursor = conn.cursor()

    client_payout_addr = request.args.get('payout_address')
    cursor.execute("INSERT INTO bids (address) VALUES (%s) RETURNING id;", (client_payout_addr,))
    client_bid_number = cursor.fetchone()[0]

    # grabbing all of these things at once to minimize the number of requests to the db
    cursor.execute("SELECT round_number, winning_bid_number, pot_size FROM rounds ORDER BY round_number desc LIMIT 1;")
    [current_round_number, winning_bid_number, pot_size] = cursor.fetchone()

    if winning_bid_number == client_bid_number:
        waiting_to_pay = False
        prize = int(pot_size/2)
        try:
            txid = wallet.send_to(client_payout_addr, prize)
        except:
            e = sys.exc_info()[0]
            print( "<p>Error: %s</p>" % e )
            waiting_to_pay = True
            # insert into waiting db
            SQL = "INSERT INTO waiting_to_pay (bid_id, address, round, prize) values (%s, %s, %s, %s);"
            data = (client_bid_number, client_payout_addr, current_round_number, prize,)
            cursor.execute(SQL, data)

        cursor.execute("UPDATE bids SET is_winner = TRUE WHERE id = %s;", (client_bid_number,))

        random_number = math.floor(random.random()*(10*(2**(current_round_number + 1)))) + 1
        new_pot_size = prize + (random_number * 1000)

        SQL = "INSERT INTO rounds (winning_bid_number, pot_size) VALUES (%s, %s);"
        data = (random_number, new_pot_size,)
        cursor.execute(SQL, data)

        conn.commit()
        cursor.close() 

        if waiting_to_pay:
            return "You win! You will be paid " + str(prize) + " Satoshis (" + str(prize/100000000) + " bitcoins), but due to the way the 21 handles sends we have to wait for our last payment to be validated before we can pay you. It will be sent soon!"
        else:
            return "You win! You have been paid " + str(prize) + " Satoshis (" + str(prize/100000000) + " bitcoins!"
    else:
        conn.commit()
        cursor.close() 

        return "Sorry! Try again!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
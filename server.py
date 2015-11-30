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
    conn = psycopg2.connect(database=os.environ.get("DB_PSWD"), user=os.environ.get("DB_USER"), password=os.environ.get("DATABASE_PASSWORD"))
    cursor = conn.cursor()
    # can just grab the data here
    cursor.execute("SELECT * FROM rounds ORDER BY round_number asc;") # need to modify to not return the most recent
    result = cursor.fetchall()
    length = len(result)
    data = [i for i in range(length)]
    for d in result:
        data[d[0] - 1] = [d[0], d[1], d[2]]
    data[length - 1][1] = -1
    return render_template('index.html', data=data)

# machine-payable endpoint that pays user if they are the winning request number
@app.route('/lotterMe')
@payment.required(200)
def lottery():
    conn = psycopg2.connect(database=os.environ.get("DB_PSWD"), user=os.environ.get("DB_USER"), password=os.environ.get("DATABASE_PASSWORD"))
    cursor = conn.cursor()

    client_payout_addr = request.args.get('payout_address')
    cursor.execute("INSERT INTO bids (address) VALUES (%s) RETURNING id;", (client_payout_addr,))
    client_bid_number = cursor.fetchone()[0]

    # grabbing all of these things at once to minimize the number of requests to the db
    cursor.execute("SELECT round_number, winning_bid_number, pot_size FROM rounds ORDER BY round_number desc LIMIT 1;")
    [current_round_number, winning_bid_number, pot_size] = cursor.fetchone()

    if winning_bid_number == client_bid_number:
        waiting_to_pay = False
        try:
            txid = wallet.send_to(client_payout_addr, (pot_size/2))
        except:
            print("IN exception")
            waiting_to_pay = True
            # insert into waiting db
            SQL = "INSERT INTO waiting_to_pay (bid_id, address, round, prize) values (%s, %s, %s, %s)"
            data = (client_bid_number, client_payout_addr, current_round_number, (pot_size/2),)
            print('got here')
            try:
                cursor.execute(data, SQL)
            except Exception, e:
                print(e)
                pass

        cursor.execute("UPDATE bids SET is_winner = TRUE WHERE id = %s;", (client_bid_number,))

        random_number = math.floor(random.random()*(10*(2**(current_round_number + 1)))) + 1
        new_pot_size = (pot_size/2) + (random_number * 1000)

        SQL = "INSERT INTO rounds (winning_bid_number, pot_size) VALUES (%s, %s);"
        data = (random_number, new_pot_size,)
        cursor.execute(SQL, data)

        conn.commit()
        cursor.close() 

        if waiting_to_pay:
            return "You win! You will be paid " + str(pot_size/100000000) + " bitcoins, but due to the way the 21 handles sends we have to wait for our last payment to be validated before we can pay you. The money will be sent soon!"
        else:
            return "You win! You have been paid " + str(pot_size/100000000) + " bitcoins!"
    else:
        conn.commit()
        cursor.close() 

        return "Sorry! Try again!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
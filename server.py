import os
import json
import random

# import flask web microframework
from flask import Flask
from flask import request

# import from the 21 Developer Library
from two1.lib.wallet import Wallet
from two1.lib.bitserv.flask import Payment

app = Flask(__name__)
wallet = Wallet()
payment = Payment(app, wallet)

conn = psycopg2.connect(database="lottery", user="postgres",)
cursor = conn.cursor()

cursor.execute("SELECT hit_number from lottery;")
print(cursor.fetchone()[0])



if __name__ == '__main__':
    app.run(host='0.0.0.0')
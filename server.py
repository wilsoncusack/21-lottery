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

# endpoint to get a question from the server
totalPlays = 0
@app.route('/bet')
@payment.required(1000)
def get_bet():
    print(request)
    totalPlays += 1
    print(totalPlays)
    return "you're better number X, once 10 betters have played, a winner will be chosen"

# machine-payable endpoint that pays user if answer is correct
if __name__ == '__main__':
    app.run(host='0.0.0.0')




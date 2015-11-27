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

question_bank = {
    'Who is the inventor of Bitcoin': 'Satoshi Nakamoto',
    'How many satoshis are in a bitcoin': '100000000',
    'What is the current coinbase reward (in BTC) for mining a block': '25'
}

question_list = list(question_bank.keys())

# endpoint to get a question from the server
@app.route('/lottery')
def get_question():
    return question_list[random.randrange(0,len(question_list))]

# machine-payable endpoint that pays user if answer is correct
@app.route('/lottery/<int:amount>')
@payment.required(amount)
def win_money():
    randomNumber = rand.randrange(0,10)
    client_payout_addr = request.args.get('payout_address')
    if randomNumber >= 8
        wallet.send_to(client_payout_addr, (amount * 2))
    else:
        wallet.send_to(client_payout_addr, (amount/2))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
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
@app.route('/question')
def get_question():
    return question_list[random.randrange(0,len(question_list))]

# machine-payable endpoint that pays user if answer is correct
@app.route('/play')
@payment.required(1000)
def answer_question():

    # extract answer from client request
    answer = request.args.get('selection')

    # extract payout address from client address
    client_payout_addr = request.args.get('payout_address')

    # extract question from client request
    client_question = request.args.get('question')

    # check if answer is correct
    if answer.lower() == question_bank[client_question].lower():
        txid = wallet.send_to(client_payout_addr, 2000)
        return "Correct!"
    else:
        return "Incorrect response."

if __name__ == '__main__':
    app.run(host='0.0.0.0')
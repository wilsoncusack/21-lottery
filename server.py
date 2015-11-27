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
@app.route('/bet')
@payment.required(1000)
def get_bet():
    return "you're better number X, once 10 betters have played, a winner will be chosen"

# machine-payable endpoint that pays user if answer is correct
# @app.route('/play')
# @payment.required(1000)
# def answer_question():

#     # extract answer from client request
#     answer = request.args.get('selection')

#     # extract payout address from client address
#     client_payout_addr = request.args.get('payout_address')

#     # extract question from client request
#     client_question = request.args.get('question')

#     # check if answer is correct
#     if answer.lower() == question_bank[client_question].lower():
#         txid = wallet.send_to(client_payout_addr, 2000)
#         return "Correct!"
#     else:
#         return "Incorrect response."

if __name__ == '__main__':
    app.run(host='0.0.0.0')
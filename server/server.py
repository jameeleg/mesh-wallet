from flask import Flask, jsonify, abort, request

from wallet_manager import WalletManager
from utils import is_valid_request

app = Flask(__name__)
wallet = WalletManager()


@app.route('/')
def index():
    return 'Wallet app'


@app.route('/balance', methods=['GET'])
def handle_balance():
    return jsonify(wallet.get_balance())


@app.route('/history', methods=['GET'])
def handle_history():
    return jsonify(wallet.get_history())


@app.route('/add', methods=['POST'])
def handle_deposit():
    request_data = request.get_json()

    # sanity check on user input
    valid, amount = is_valid_request(request_data)
    if not valid:
        return abort(400, "User entered bad request")  # 401 bad request

    new_balance = wallet.deposit(amount)
    return jsonify(new_balance)


@app.route('/subtract', methods=['POST'])
def handle_withdraw():
    request_data = request.get_json()
    # sanity check on user input
    valid, amount = is_valid_request(request_data)
    if not valid:
        return abort(400, "User entered bad request")  # 401 bad request

    ok, new_balance = wallet.withdraw(amount)
    if not ok:
        return abort(400, "Not enough money in the wallet")  # I'm not sure if it should be 400??
    return jsonify(new_balance)


if __name__ == '__main__':
    # debug mode
    app.run(host='localhost', debug=True, port=6060)
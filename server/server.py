from flask import Flask, jsonify, abort, request
from wallet_manager import WalletManager

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

    new_balance = wallet.withdraw(amount)
    return jsonify(new_balance)


def is_valid_request(request_data):
    # try get 'amount' from request body
    # if there is no amount, then return -1
    amount = request_data.get('amount', -1)
    if amount > 0:
        return True, amount

    return False, None


if __name__ == '__main__':
    # debug mode
    app.run(host='localhost', debug=True, port=6060)
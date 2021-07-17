# Wallet Manager Server
In this tiny project, I introduce a simple implementation of a webserver that manages a wallet.
The webserver supports the following features:
1. Get the current balance of the wallet
2. Show the history of the operations in the wallet
3. Deposit amount to the wallet
4. Withdraws amount from the wallet

## Stack
The webserver built on top of Flask framework.
The webserver is written in python. Manages in-memory a wallet.
There 3 files:
1. `server.py`
2. `wallet_manager.py`
3. `utils.py`
The file `server.py` is the executable file. Using the Flask framework, we define the endpoints and the handlers.
The server, on startup, initiates an instance of type `WalletManager`, and uses it to server requests of `balance`, 
`history`, `add` and `sub`.

`WalletManager` class is thread safe. It means that it can be called from many threads and keep the data synchronized and safe.
The class exposes APIs that are thread-safe. (note that method that starts with `_` is internal method and should not be accessed out side the `WalletManager` class)

`utils.py` - contains some helpers methods

## Weber server APIs
1. `GET /` should return `Wallet app`
2. `GET /history` returns the history of the operations in the wallet
3. `GET /balance` returns the balance of the wallet the timestamp of the last operation
4. `POST /add` Deposits `amount` to the wallet
4. `POST /sub` Withdraws `amount` from the wallet

## Operations APIs
Both `/add` and `/sub` expect a post HTTP request with a json of `{"amount: <number>}` in body of the request.
You need to add a the following header in your HTTP Post request `"Content-Type": "application/json"`

## Running dev webserver
1. `$ git clone git@github.com:jameeleg/mesh-wallet.git`
2. `$ cd mesh-wallet/server`
3. `$ python3 -m venv venv`
4. `$ . venv/bin/activate`
5. `$ pip install Flask`
6. Start the server: `$ python3 server.py`
Then you should see the output ```Running on http://localhost:6060/```


## (Testing) Prepared postman collection for you
I've attached a file in `mesh-wallet/Wallet.postman_collection.jos` in the repository.
You can import it in your Postman app and invoke HTTP requests from the collection I've created.
You can add, remove, update the requests as you want.

You can find also `Bad requests` in the collection such as negative `amount` or a request with `amount`  in the body.

NOTE: requests in the collections goes to `localhost:6060`. If you change the port, you should change the port in the postman collection as well.

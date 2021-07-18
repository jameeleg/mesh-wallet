import threading
from datetime import datetime
from enum import Enum

from utils import truncate_num


class Operations(Enum):
    ADD = 1
    SUBTRACT = 2


class WalletManager(object):
    def __init__(self, initial_balance=0.00):
        self._balance = initial_balance
        self._history = []
        self._lock = threading.Lock()

    # EXTERNAL APIS #

    def get_balance(self):
        with self._lock:
            if len(self._history) == 0:
                return {"balance": 0, "ts": "N/A"}

            last_operation = self._history[-1]
            return {"balance": last_operation["balance"], "ts": last_operation["ts"]}

    def get_history(self):
        # since we have a lock on deposit and withdraw,
        # no other thread can access while the working thread still working
        # So _history will be sorted by ts
        return self._history

    def deposit(self, amount):
        if amount < 0:
            return False, "Cannot deposit negative amount"
        with self._lock:
            self._balance = truncate_num(self._balance + amount)
            self._add_operation_to_history(Operations.ADD.name, amount)
            return True, self._balance  # return the balance after fulfilling the deposit operation

    def withdraw(self, amount):
        with self._lock:
            if amount > self._balance:
                # if we don't have enough balance, we don't add the operation to history
                # we keep in history, the operations that succeeded.
                return False, "No enough balance in the wallet"
            if amount <= 0:
                return False, "Cannot withdraw negative amount"

            self._balance = truncate_num(self._balance - amount)
            self._add_operation_to_history(Operations.SUBTRACT.name, amount)
            return True, self._balance  # return the balance after fulfilling the withdraw operation

    # END OF EXTERNAL APIS #

    # INTERNAL METHODS #
    def _add_operation_to_history(self, ops, amount):
        # we don't need to lock here, the thread already have the lock from
        # the calling method
        self._history.append({
            "operation": ops,
            "ts": datetime.now(),
            "amount": amount,
            "balance": self._balance,
        })

    # END OF INTERNAL METHODS #
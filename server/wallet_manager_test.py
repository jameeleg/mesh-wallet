import sys
import threading
import time
import unittest

from wallet_manager import WalletManager


class BankAccountTest(unittest.TestCase):
    def test_newly_opened_account_has_zero_balance(self):
        wallet = WalletManager()
        self.assertEqual(wallet.get_balance(),  {'balance': 0, 'ts': 'N/A'})

    def test_can_deposit_positive_amount(self):
        wallet = WalletManager()
        is_ok, result = wallet.deposit(100)
        self.assertEqual(is_ok, True)
        self.assertEqual(result, 100)

    def test_cannot_deposit_negative_amount(self):
        wallet = WalletManager()
        is_ok, result = wallet.deposit(-100)
        self.assertEqual(is_ok, False)
        self.assertEqual(result, "Cannot deposit negative amount")
        self.assertEqual(wallet.get_balance(), {'balance': 0, 'ts': 'N/A'})

    def test_can_withdraw_positive_amount(self):
        wallet = WalletManager(100)
        is_ok, result = wallet.withdraw(50)
        self.assertEqual(is_ok, True)
        self.assertEqual(result, 50)

    def test_cannot_withdraw_negative_amount(self):
        wallet = WalletManager(100)
        is_ok, result = wallet.withdraw(-50)
        self.assertEqual(is_ok, False)
        self.assertEqual(result, "Cannot withdraw negative amount")

    def test_cannot_withdraw_amount_bigger_balance(self):
        wallet = WalletManager(100)
        is_ok, result = wallet.withdraw(300)
        self.assertEqual(is_ok, False)
        self.assertEqual(result, "No enough balance in the wallet")

    def test_can_deposit_money_sequentially(self):
        wallet = WalletManager()
        wallet.deposit(100)
        wallet.deposit(50)

        self.assertEqual(wallet.get_balance()['balance'], 150)

    def test_can_withdraw_money_sequentially(self):
        wallet = WalletManager(100)
        wallet.withdraw(20)
        wallet.withdraw(80)

        self.assertEqual(wallet.get_balance()['balance'], 0)

    def test_can_handle_concurrent_transactions(self):
        wallet = WalletManager()
        wallet.deposit(1000)

        self.adjust_balance_concurrently(wallet)

        self.assertEqual(wallet.get_balance()['balance'], 1000)

    def adjust_balance_concurrently(self, account):
        def transact():
            account.deposit(5)
            time.sleep(0.001)
            account.withdraw(5)

        # Greatly improve the chance of an operation being interrupted
        # by thread switch, thus testing synchronization effectively
        try:
            sys.setswitchinterval(1e-12)
        except AttributeError:
            # For Python 2 compatibility
            sys.setcheckinterval(1)

        threads = [threading.Thread(target=transact) for _ in range(1000)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    # Utility functions
    def assertRaisesWithMessage(self, exception):
        return self.assertRaisesRegex(exception, r".+")


if __name__ == '__main__':
    unittest.main()

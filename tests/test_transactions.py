import unittest
from src.models.account import SavingsAccount
from src.services.transaction_service import TransactionService

class TestBankingSystem(unittest.TestCase):
    def setUp(self):
        self.savings_acc = SavingsAccount("ACC001", "CUST001", 1000)
        self.transaction_service = TransactionService()
    
    def test_deposit(self):
        self.assertTrue(self.savings_acc.deposit(500))
        self.assertEqual(self.savings_acc.balance, 1500)
    
    def test_withdraw_sufficient_funds(self):
        self.assertTrue(self.savings_acc.withdraw(300))
        self.assertEqual(self.savings_acc.balance, 700)
    
    def test_withdraw_insufficient_funds(self):
        self.assertFalse(self.savings_acc.withdraw(1500))
        self.assertEqual(self.savings_acc.balance, 1000)

if __name__ == '__main__':
    unittest.main()
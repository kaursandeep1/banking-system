import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.account import SavingsAccount, CheckingAccount, AccountType
from src.services.account_service import AccountService

class TestAccounts(unittest.TestCase):
    def setUp(self):
        self.account_service = AccountService()
        self.customer_id = "TEST_CUST_001"
    
    def test_account_creation(self):
        account = self.account_service.create_account(self.customer_id, AccountType.SAVINGS, 1000)
        self.assertEqual(account.customer_id, self.customer_id)
        self.assertEqual(account.balance, 1000)
        self.assertEqual(account.account_type, AccountType.SAVINGS)
    
    def test_deposit_functionality(self):
        account = self.account_service.create_account(self.customer_id, AccountType.SAVINGS, 500)
        initial_balance = account.balance
        
        # Test valid deposit
        success = account.deposit(300)
        self.assertTrue(success)
        self.assertEqual(account.balance, initial_balance + 300)
        
        # Test invalid deposit (negative amount)
        success = account.deposit(-100)
        self.assertFalse(success)
        self.assertEqual(account.balance, initial_balance + 300)
    
    def test_withdrawal_functionality(self):
        account = self.account_service.create_account(self.customer_id, AccountType.SAVINGS, 1000)
        
        # Test valid withdrawal
        success = account.withdraw(300)
        self.assertTrue(success)
        self.assertEqual(account.balance, 700)
        
        # Test overdraft protection
        success = account.withdraw(800)
        self.assertFalse(success)
        self.assertEqual(account.balance, 700)

if __name__ == '__main__':
    unittest.main()
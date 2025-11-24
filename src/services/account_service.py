from models.account import SavingsAccount, CheckingAccount, AccountType
import secrets

class AccountService:
    def __init__(self):
        self.accounts = {}
    
    def create_account(self, customer_id, account_type=AccountType.SAVINGS, initial_balance=0):
        account_number = self._generate_account_number()
        
        if account_type == AccountType.SAVINGS:
            account = SavingsAccount(account_number, customer_id, initial_balance)
        else:
            account = SavingsAccount(account_number, customer_id, initial_balance)
        
        self.accounts[account_number] = account
        return account
    
    def _generate_account_number(self):
        return f"ACC{secrets.token_hex(6).upper()}"
    
    def get_account(self, account_number):
        return self.accounts.get(account_number)
    
    def get_customer_accounts(self, customer_id):
        return [acc for acc in self.accounts.values() if acc.customer_id == customer_id]
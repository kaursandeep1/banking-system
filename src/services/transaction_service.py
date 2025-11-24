from models.transaction import Transaction
from models.account import Account

class TransactionService:
    def __init__(self):
        self.transaction_history = []
    
    def transfer(self, from_account, to_account, amount, description=""):
        if not from_account or not to_account:
            return False, "Invalid accounts"
        
        if from_account.withdraw(amount):
            to_account.deposit(amount)
            
            # Record transaction
            transaction = Transaction(amount, "TRANSFER", 
                                    f"Transfer to {to_account.account_number}: {description}")
            self.transaction_history.append(transaction)
            return True, "Transfer successful"
        
        return False, "Insufficient funds"
    
    def get_account_statement(self, account, days=30):
        cutoff_date = datetime.now() - timedelta(days=days)
        return [t for t in account.transactions if t.timestamp >= cutoff_date]
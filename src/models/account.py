from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import secrets

class AccountType(Enum):
    SAVINGS = "Savings"
    CHECKING = "Checking"

class Account(ABC):
    def __init__(self, account_number, customer_id, balance=0, account_type=AccountType.SAVINGS):
        self.account_number = account_number
        self.customer_id = customer_id
        self._balance = balance
        self.account_type = account_type
        self.transactions = []
        self.created_at = datetime.now()
    
    @property
    def balance(self):
        return self._balance
    
    @abstractmethod
    def withdraw(self, amount):
        pass
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            transaction = Transaction(amount, "DEPOSIT")
            self.transactions.append(transaction)
            return True
        return False

class SavingsAccount(Account):
    def __init__(self, account_number, customer_id, balance=0):
        super().__init__(account_number, customer_id, balance, AccountType.SAVINGS)
        self.interest_rate = 0.02
        self.minimum_balance = 0
    
    def withdraw(self, amount):
        if amount > 0 and self._balance - amount >= self.minimum_balance:
            self._balance -= amount
            transaction = Transaction(amount, "WITHDRAWAL")
            self.transactions.append(transaction)
            return True
        return False

class CheckingAccount(Account):
    def __init__(self, account_number, customer_id, balance=0):
        super().__init__(account_number, customer_id, balance, AccountType.CHECKING)
        self.overdraft_limit = 100
        self.transaction_fee = 0.50
    
    def withdraw(self, amount):
        if amount > 0 and self._balance - amount >= -self.overdraft_limit:
            self._balance -= amount
            # Apply transaction fee for checking accounts
            if amount > 0:
                self._balance -= self.transaction_fee
            
            transaction = Transaction(amount, "WITHDRAWAL")
            self.transactions.append(transaction)
            return True
        return False

class Transaction:
    def __init__(self, amount, transaction_type, description=""):
        self.transaction_id = secrets.token_hex(8)
        self.amount = amount
        self.type = transaction_type
        self.description = description
        self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'type': self.type,
            'description': self.description,
            'timestamp': self.timestamp.isoformat()
        }
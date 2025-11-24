from datetime import datetime
import secrets

class TransactionType:
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER = "TRANSFER"

class Transaction:
    def __init__(self, amount, transaction_type, description="", from_account=None, to_account=None):
        self.transaction_id = secrets.token_hex(8)
        self.amount = amount
        self.type = transaction_type
        self.description = description
        self.from_account = from_account
        self.to_account = to_account
        self.timestamp = datetime.now()
        self.status = "COMPLETED"
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'amount': self.amount,
            'type': self.type,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status
        }
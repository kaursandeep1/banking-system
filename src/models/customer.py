import hashlib
import secrets
from datetime import datetime

class Customer:
    def __init__(self, customer_id, name, email, password):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self._password_hash, self.salt = self._hash_password(password)
        self.accounts = []
        self.created_at = datetime.now()
    
    def _hash_password(self, password):
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode(), 
            salt.encode(), 
            100000
        )
        return password_hash, salt
    
    def verify_password(self, password):
        test_hash = hashlib.pbkdf2_hmac(
            'sha256', 
            password.encode(), 
            self.salt.encode(), 
            100000
        )
        return self._password_hash == test_hash
    
    def to_dict(self):
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'accounts_count': len(self.accounts)
        }
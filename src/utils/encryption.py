import hashlib
import secrets
import base64

class EncryptionUtils:
    @staticmethod
    def generate_salt(length=16):
        return secrets.token_hex(length)
    
    @staticmethod
    def hash_password(password, salt):
        """Hash password using PBKDF2"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt.encode(),
            100000
        )
    
    @staticmethod
    def generate_account_number():
        """Generate secure account number"""
        return f"ACC{secrets.token_hex(6).upper()}"
    
    @staticmethod
    def generate_customer_id():
        """Generate secure customer ID"""
        return f"CUST{secrets.token_hex(4).upper()}"
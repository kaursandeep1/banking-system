import re
from datetime import datetime

class Validators:
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        return True, "Password is valid"
    
    @staticmethod
    def validate_amount(amount):
        """Validate transaction amount"""
        try:
            amount_float = float(amount)
            if amount_float <= 0:
                return False, "Amount must be positive"
            if amount_float > 1000000:  # Limit to 1 million
                return False, "Amount exceeds maximum limit"
            return True, amount_float
        except ValueError:
            return False, "Invalid amount format"
    
    @staticmethod
    def validate_date(date_string):
        """Validate date format"""
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
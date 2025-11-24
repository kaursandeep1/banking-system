import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.models.customer import Customer
from src.services.auth_service import AuthService
from src.utils.validators import Validators

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthService()
        self.test_email = "test@example.com"
        self.test_password = "SecurePass123"
    
    def test_customer_creation(self):
        customer = Customer("TEST123", "John Doe", self.test_email, self.test_password)
        self.assertEqual(customer.name, "John Doe")
        self.assertEqual(customer.email, self.test_email)
        self.assertTrue(customer.verify_password(self.test_password))
    
    def test_password_hashing(self):
        customer1 = Customer("TEST1", "User1", "user1@test.com", "SamePassword123")
        customer2 = Customer("TEST2", "User2", "user2@test.com", "SamePassword123")
        
        # Same password should have different hashes due to different salts
        self.assertNotEqual(customer1._password_hash, customer2._password_hash)
    
    def test_email_validation(self):
        self.assertTrue(Validators.validate_email("valid@email.com"))
        self.assertFalse(Validators.validate_email("invalid-email"))
        self.assertFalse(Validators.validate_email("missing@domain"))
    
    def test_password_validation(self):
        # Test weak password
        is_valid, message = Validators.validate_password("weak")
        self.assertFalse(is_valid)
        
        # Test strong password
        is_valid, message = Validators.validate_password("StrongPass123")
        self.assertTrue(is_valid)

if __name__ == '__main__':
    unittest.main()
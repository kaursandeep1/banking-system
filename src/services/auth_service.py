from models.customer import Customer
import secrets

class AuthService:
    def __init__(self):
        self.customers = {}
        self.sessions = {}
    
    def register_customer(self, name, email, password):
        if email in [c.email for c in self.customers.values()]:
            return None, "Email already registered"
        
        customer_id = secrets.token_hex(8)
        customer = Customer(customer_id, name, email, password)
        self.customers[customer_id] = customer
        return customer, "Registration successful"
    
    def login(self, email, password):
        for customer in self.customers.values():
            if customer.email == email and customer.verify_password(password):
                session_token = secrets.token_hex(16)
                self.sessions[session_token] = customer.customer_id
                return session_token, customer, "Login successful"
        return None, None, "Invalid credentials"
    
    def get_customer_from_session(self, session_token):
        customer_id = self.sessions.get(session_token)
        return self.customers.get(customer_id)
from services.auth_service import AuthService
from services.account_service import AccountService
from services.transaction_service import TransactionService
from models.account import AccountType
from utils.validators import Validators
from utils.logger import logger

class BankingSystem:
    def __init__(self):
        self.auth_service = AuthService()
        self.account_service = AccountService()
        self.transaction_service = TransactionService()
        self.current_session = None
        self.current_customer = None
    
    def register(self):
        print("\n=== Customer Registration ===")
        name = input("Full Name: ")
        email = input("Email: ")
        password = input("Password: ")
        
        # Validate inputs
        if not Validators.validate_email(email):
            print("❌ Invalid email format")
            return
        
        is_valid, message = Validators.validate_password(password)
        if not is_valid:
            print(f"❌ {message}")
            return
        
        customer, message = self.auth_service.register_customer(name, email, password)
        if customer:
            print(f"✅ {message}")
            print(f"📋 Customer ID: {customer.customer_id}")
            logger.log_security_event("REGISTRATION", customer.customer_id, "New customer registered")
        else:
            print(f"❌ {message}")
    
    def login(self):
        print("\n=== Customer Login ===")
        email = input("Email: ")
        password = input("Password: ")
        
        session_token, customer, message = self.auth_service.login(email, password)
        if customer:
            self.current_session = session_token
            self.current_customer = customer
            print(f"✅ {message}")
            print(f"👋 Welcome back, {customer.name}!")
            logger.log_security_event("LOGIN", customer.customer_id, "Successful login")
            return True
        else:
            print(f"❌ {message}")
            logger.log_security_event("LOGIN_FAILED", "UNKNOWN", f"Failed login attempt for {email}")
            return False
    
    def create_account(self):
        if not self.current_customer:
            print("❌ Please login first")
            return
        
        print("\n=== Create New Account ===")
        print("1. Savings Account")
        print("2. Checking Account")
        choice = input("Select account type (1-2): ")
        
        account_type = AccountType.SAVINGS if choice == "1" else AccountType.CHECKING
        initial_deposit = input("Initial deposit amount: $")
        
        is_valid, result = Validators.validate_amount(initial_deposit)
        if not is_valid:
            print(f"❌ {result}")
            return
        
        account = self.account_service.create_account(
            self.current_customer.customer_id, 
            account_type, 
            result
        )
        self.current_customer.accounts.append(account)
        print(f"✅ Account created successfully!")
        print(f"📋 Account Number: {account.account_number}")
        print(f"💰 Current Balance: ${account.balance:.2f}")
        logger.log_transaction("ACCOUNT_CREATION", account.account_number, result)
    
    def show_dashboard(self):
        if not self.current_customer:
            print("❌ Please login first")
            return
        
        accounts = self.account_service.get_customer_accounts(self.current_customer.customer_id)
        
        print(f"\n=== Dashboard - {self.current_customer.name} ===")
        print(f"📧 Email: {self.current_customer.email}")
        print(f"🆔 Customer ID: {self.current_customer.customer_id}")
        print(f"📅 Member since: {self.current_customer.created_at.strftime('%Y-%m-%d')}")
        
        if not accounts:
            print("\n📭 No accounts found. Create your first account!")
            return
        
        total_balance = sum(acc.balance for acc in accounts)
        print(f"\n💰 Total Balance: ${total_balance:.2f}")
        print("\n🏦 Your Accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"   {i}. {account.account_number} | {account.account_type.value} | Balance: ${account.balance:.2f}")
    
    def deposit(self):
        if not self.current_customer:
            print("❌ Please login first")
            return
        
        self.show_dashboard()
        accounts = self.account_service.get_customer_accounts(self.current_customer.customer_id)
        
        if not accounts:
            return
        
        try:
            acc_choice = int(input("\nSelect account number (1-{}): ".format(len(accounts)))) - 1
            if acc_choice < 0 or acc_choice >= len(accounts):
                print("❌ Invalid account selection")
                return
            
            account = accounts[acc_choice]
            amount = input("Deposit amount: $")
            
            is_valid, result = Validators.validate_amount(amount)
            if not is_valid:
                print(f"❌ {result}")
                return
            
            if account.deposit(result):
                print(f"✅ Deposited ${result:.2f} to {account.account_number}")
                print(f"💰 New Balance: ${account.balance:.2f}")
                logger.log_transaction("DEPOSIT", account.account_number, result)
            else:
                print("❌ Deposit failed")
                logger.log_transaction("DEPOSIT", account.account_number, result, "FAILED")
                
        except ValueError:
            print("❌ Invalid input")
    
    def run(self):
        print("🏦 Welcome to Banking System Simulation")
        
        while True:
            print("\n=== Main Menu ===")
            print("1. Register")
            print("2. Login")
            print("3. Create Account")
            print("4. View Dashboard")
            print("5. Deposit Money")
            print("6. Exit")
            
            choice = input("Select option (1-6): ")
            
            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                self.create_account()
            elif choice == "4":
                self.show_dashboard()
            elif choice == "5":
                self.deposit()
            elif choice == "6":
                print("👋 Thank you for using our banking system!")
                break
            else:
                print("❌ Invalid option")

if __name__ == "__main__":
    bank = BankingSystem()
    bank.run()
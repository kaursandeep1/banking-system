import logging
from datetime import datetime

class BankLogger:
    def __init__(self, log_file='banking_system.log'):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BankingSystem')
    
    def log_transaction(self, transaction_type, account_number, amount, status="SUCCESS"):
        self.logger.info(
            f"TRANSACTION - Type: {transaction_type}, "
            f"Account: {account_number}, "
            f"Amount: ${amount:.2f}, "
            f"Status: {status}"
        )
    
    def log_security_event(self, event_type, customer_id, details):
        self.logger.warning(
            f"SECURITY - Event: {event_type}, "
            f"Customer: {customer_id}, "
            f"Details: {details}"
        )
    
    def log_error(self, error_type, details):
        self.logger.error(f"ERROR - Type: {error_type}, Details: {details}")

# Global logger instance
logger = BankLogger()
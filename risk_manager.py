from config import Config
from logger import setup_logger
from datetime import datetime, timedelta

logger = setup_logger()

class RiskManager:
    def __init__(self, initial_balance=None):
        """Initialize risk manager"""
        self.initial_balance = initial_balance or Config.INITIAL_BALANCE
        self.current_balance = self.initial_balance
        self.target_profit = Config.TARGET_PROFIT
        self.deadline = datetime.now() + timedelta(days=Config.DEADLINE_DAYS)
        self.max_loss = self.initial_balance * (Config.MAX_LOSS_PERCENT / 100)
        self.positions = []
        logger.info(f"Risk Manager initialized - Balance: ${self.initial_balance}, Target: ${self.target_profit}")
    
    def calculate_position_size(self, current_price):
        """Calculate position size based on risk"""
        try:
            risk_amount = self.initial_balance * (Config.STOP_LOSS_PERCENT / 100)
            position_size = (risk_amount / (current_price * (Config.STOP_LOSS_PERCENT / 100))) * Config.LEVERAGE
            logger.info(f"Position size calculated: {position_size:.4f}")
            return position_size
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0
    
    def check_stop_loss(self, entry_price, current_price):
        """Check if stop loss is hit"""
        stop_loss_price = entry_price * (1 - Config.STOP_LOSS_PERCENT / 100)
        if current_price <= stop_loss_price:
            logger.warning(f"Stop loss triggered at ${current_price}")
            return True
        return False
    
    def check_take_profit(self, entry_price, current_price):
        """Check if take profit is hit"""
        take_profit_price = entry_price * (1 + Config.TAKE_PROFIT_PERCENT / 100)
        if current_price >= take_profit_price:
            logger.info(f"Take profit triggered at ${current_price}")
            return True
        return False
    
    def update_balance(self, profit_loss):
        """Update current balance"""
        self.current_balance += profit_loss
        profit_percent = ((self.current_balance - self.initial_balance) / self.initial_balance) * 100
        logger.info(f"Balance updated: ${self.current_balance:.2f} ({profit_percent:+.2f}%)")
    
    def check_deadline(self):
        """Check if deadline has passed"""
        if datetime.now() > self.deadline:
            logger.warning(f"Deadline passed: {self.deadline}")
            return True
        return False
    
    def check_target_reached(self):
        """Check if target profit reached"""
        profit = self.current_balance - self.initial_balance
        if profit >= self.target_profit:
            logger.info(f"Target profit reached! Profit: ${profit:.2f}")
            return True
        return False
    
    def check_max_loss_exceeded(self):
        """Check if maximum loss exceeded"""
        loss = self.initial_balance - self.current_balance
        if loss >= self.max_loss:
            logger.error(f"Maximum loss exceeded: ${loss:.2f}")
            return True
        return False
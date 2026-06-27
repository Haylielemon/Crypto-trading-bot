import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Binance API
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
    
    # Trading Parameters
    TRADING_PAIR = os.getenv('TRADING_PAIR', 'BTCUSDT')
    INITIAL_BALANCE = float(os.getenv('INITIAL_BALANCE', 50))
    TARGET_PROFIT = float(os.getenv('TARGET_PROFIT', 5000))
    DEADLINE_DAYS = int(os.getenv('DEADLINE_DAYS', 14))
    
    # Risk Management
    MAX_LOSS_PERCENT = float(os.getenv('MAX_LOSS_PERCENT', 10))
    TAKE_PROFIT_PERCENT = float(os.getenv('TAKE_PROFIT_PERCENT', 20))
    STOP_LOSS_PERCENT = float(os.getenv('STOP_LOSS_PERCENT', 5))
    LEVERAGE = float(os.getenv('LEVERAGE', 2))
    
    # Strategy Parameters
    RSI_PERIOD = int(os.getenv('RSI_PERIOD', 14))
    RSI_OVERBOUGHT = int(os.getenv('RSI_OVERBOUGHT', 70))
    RSI_OVERSOLD = int(os.getenv('RSI_OVERSOLD', 30))
    MAC_FAST = int(os.getenv('MAC_FAST', 12))
    MAC_SLOW = int(os.getenv('MAC_SLOW', 26))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
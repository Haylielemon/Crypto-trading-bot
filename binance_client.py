from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from config import Config
from logger import setup_logger

logger = setup_logger()

class BinanceTrader:
    def __init__(self):
        """Initialize Binance client"""
        try:
            self.client = Client(Config.BINANCE_API_KEY, Config.BINANCE_API_SECRET)
            self.trading_pair = Config.TRADING_PAIR
            logger.info(f"Binance client initialized for {self.trading_pair}")
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            raise
    
    def get_account_balance(self):
        """Get current account balance"""
        try:
            account = self.client.get_account()
            balances = {asset['asset']: float(asset['free']) for asset in account['balances']}
            logger.info(f"Account balance retrieved: {balances}")
            return balances
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e}")
            return None
    
    def get_current_price(self):
        """Get current price of trading pair"""
        try:
            price = self.client.get_symbol_ticker(symbol=self.trading_pair)
            current_price = float(price['price'])
            logger.info(f"{self.trading_pair} current price: ${current_price}")
            return current_price
        except BinanceAPIException as e:
            logger.error(f"Error getting price: {e}")
            return None
    
    def get_klines(self, interval='1h', limit=100):
        """Get historical kline data"""
        try:
            klines = self.client.get_klines(symbol=self.trading_pair, interval=interval, limit=limit)
            logger.info(f"Retrieved {len(klines)} klines for {self.trading_pair}")
            return klines
        except BinanceAPIException as e:
            logger.error(f"Error getting klines: {e}")
            return None
    
    def place_buy_order(self, quantity):
        """Place a buy order"""
        try:
            order = self.client.order_market_buy(symbol=self.trading_pair, quantity=quantity)
            logger.info(f"Buy order placed: {quantity} {self.trading_pair}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error: {e}")
            return None
    
    def place_sell_order(self, quantity):
        """Place a sell order"""
        try:
            order = self.client.order_market_sell(symbol=self.trading_pair, quantity=quantity)
            logger.info(f"Sell order placed: {quantity} {self.trading_pair}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error: {e}")
            return None
    
    def get_order_status(self, order_id):
        """Check order status"""
        try:
            order = self.client.get_order(symbol=self.trading_pair, orderId=order_id)
            logger.info(f"Order {order_id} status: {order['status']}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Error getting order status: {e}")
            return None
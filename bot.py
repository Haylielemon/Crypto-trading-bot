import time
from datetime import datetime
from config import Config
from binance_client import BinanceTrader
from strategy import TradingStrategy
from risk_manager import RiskManager
from logger import setup_logger

logger = setup_logger()

class AutoTradingBot:
    def __init__(self):
        """Initialize the trading bot"""
        logger.info("=" * 50)
        logger.info("AUTO TRADING BOT INITIALIZED")
        logger.info("=" * 50)
        
        self.trader = BinanceTrader()
        self.strategy = TradingStrategy()
        self.risk_manager = RiskManager(Config.INITIAL_BALANCE)
        
        self.is_running = False
        self.current_position = None
        self.trade_count = 0
    
    def execute_trade(self, signal):
        """Execute trade based on signal"""
        try:
            current_price = self.trader.get_current_price()
            if not current_price:
                return
            
            action = signal['action']
            strength = signal['strength']
            
            if action == 'BUY' and not self.current_position:
                # Calculate position size
                position_size = self.risk_manager.calculate_position_size(current_price)
                if position_size > 0:
                    # Execute buy order
                    order = self.trader.place_buy_order(position_size)
                    if order:
                        self.current_position = {
                            'type': 'LONG',
                            'entry_price': current_price,
                            'quantity': position_size,
                            'order_id': order['orderId'],
                            'timestamp': datetime.now()
                        }
                        self.trade_count += 1
                        logger.info(f"Trade #{self.trade_count}: BUY {position_size:.4f} at ${current_price}")
            
            elif action == 'SELL' and self.current_position:
                # Execute sell order
                order = self.trader.place_sell_order(self.current_position['quantity'])
                if order:
                    exit_price = current_price
                    profit_loss = (exit_price - self.current_position['entry_price']) * self.current_position['quantity']
                    self.risk_manager.update_balance(profit_loss)
                    
                    logger.info(f"Trade #{self.trade_count}: SELL {self.current_position['quantity']:.4f} at ${exit_price}")
                    logger.info(f"Profit/Loss: ${profit_loss:.2f}")
                    
                    self.current_position = None
        
        except Exception as e:
            logger.error(f"Error executing trade: {e}")
    
    def check_exit_conditions(self):
        """Check if current position should be exited"""
        if not self.current_position:
            return
        
        try:
            current_price = self.trader.get_current_price()
            if not current_price:
                return
            
            entry_price = self.current_position['entry_price']
            
            # Check stop loss
            if self.risk_manager.check_stop_loss(entry_price, current_price):
                logger.warning(f"Stop loss hit at ${current_price}")
                self.execute_trade({'action': 'SELL', 'strength': 1.0})
                return
            
            # Check take profit
            if self.risk_manager.check_take_profit(entry_price, current_price):
                logger.info(f"Take profit hit at ${current_price}")
                self.execute_trade({'action': 'SELL', 'strength': 1.0})
                return
        
        except Exception as e:
            logger.error(f"Error checking exit conditions: {e}")
    
    def run(self, interval=60):
        """Main bot loop"""
        self.is_running = True
        logger.info(f"Bot started - Update interval: {interval}s")
        logger.info(f"Target: ${self.risk_manager.target_profit} in {Config.DEADLINE_DAYS} days")
        
        try:
            while self.is_running:
                # Check exit conditions for current position
                self.check_exit_conditions()
                
                # Get kline data
                klines = self.trader.get_klines(interval='1h', limit=100)
                if not klines:
                    time.sleep(interval)
                    continue
                
                # Generate trading signal
                signal = self.strategy.generate_signal(klines)
                
                # Execute trade if signal generated
                if signal['action'] != 'HOLD':
                    self.execute_trade(signal)
                
                # Check stop conditions
                if self.risk_manager.check_deadline():
                    logger.warning("Deadline reached - Closing all positions")
                    if self.current_position:
                        self.execute_trade({'action': 'SELL', 'strength': 1.0})
                    self.stop()
                
                if self.risk_manager.check_target_reached():
                    logger.info("Target profit reached - Closing all positions")
                    if self.current_position:
                        self.execute_trade({'action': 'SELL', 'strength': 1.0})
                    self.stop()
                
                if self.risk_manager.check_max_loss_exceeded():
                    logger.error("Maximum loss exceeded - Stopping bot")
                    if self.current_position:
                        self.execute_trade({'action': 'SELL', 'strength': 1.0})
                    self.stop()
                
                # Log current status
                logger.info(f"Bot running - Balance: ${self.risk_manager.current_balance:.2f}, Trades: {self.trade_count}")
                
                # Wait for next update
                time.sleep(interval)
        
        except KeyboardInterrupt:
            logger.info("Bot interrupted by user")
            if self.current_position:
                self.execute_trade({'action': 'SELL', 'strength': 1.0})
            self.stop()
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            if self.current_position:
                self.execute_trade({'action': 'SELL', 'strength': 1.0})
            self.stop()
    
    def stop(self):
        """Stop the bot"""
        self.is_running = False
        logger.info("=" * 50)
        logger.info("BOT STOPPED")
        logger.info(f"Final Balance: ${self.risk_manager.current_balance:.2f}")
        logger.info(f"Total Trades: {self.trade_count}")
        logger.info(f"Profit/Loss: ${self.risk_manager.current_balance - self.risk_manager.initial_balance:.2f}")
        logger.info("=" * 50)
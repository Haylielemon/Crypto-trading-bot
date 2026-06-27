import pandas as pd
import numpy as np
from config import Config
from logger import setup_logger

logger = setup_logger()

class TradingStrategy:
    def __init__(self):
        """Initialize trading strategy"""
        self.rsi_period = Config.RSI_PERIOD
        self.rsi_overbought = Config.RSI_OVERBOUGHT
        self.rsi_oversold = Config.RSI_OVERSOLD
        self.mac_fast = Config.MAC_FAST
        self.mac_slow = Config.MAC_SLOW
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        try:
            delta = pd.Series(prices).diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            logger.info(f"RSI calculated: {rsi.iloc[-1]:.2f}")
            return rsi.iloc[-1]
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return None
    
    def calculate_macd(self, prices):
        """Calculate MACD (Moving Average Convergence Divergence)"""
        try:
            prices_series = pd.Series(prices)
            exp1 = prices_series.ewm(span=self.mac_fast, adjust=False).mean()
            exp2 = prices_series.ewm(span=self.mac_slow, adjust=False).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9, adjust=False).mean()
            histogram = macd - signal
            logger.info(f"MACD calculated: {macd.iloc[-1]:.4f}")
            return macd.iloc[-1], signal.iloc[-1], histogram.iloc[-1]
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return None, None, None
    
    def calculate_sma(self, prices, period=20):
        """Calculate Simple Moving Average"""
        try:
            sma = pd.Series(prices).rolling(window=period).mean()
            logger.info(f"SMA({period}) calculated: {sma.iloc[-1]:.4f}")
            return sma.iloc[-1]
        except Exception as e:
            logger.error(f"Error calculating SMA: {e}")
            return None
    
    def generate_signal(self, klines):
        """Generate trading signal based on strategy"""
        try:
            prices = [float(kline[4]) for kline in klines]  # closing prices
            
            # Calculate indicators
            rsi = self.calculate_rsi(prices, self.rsi_period)
            macd, signal, histogram = self.calculate_macd(prices)
            sma_20 = self.calculate_sma(prices, 20)
            sma_50 = self.calculate_sma(prices, 50)
            
            signal_result = {'action': 'HOLD', 'strength': 0}
            
            # Buy signal: RSI oversold + MACD crossover
            if rsi and rsi < self.rsi_oversold and macd and signal:
                if macd > signal and histogram > 0:
                    signal_result = {'action': 'BUY', 'strength': 0.8}
                    logger.info(f"BUY signal generated - RSI: {rsi:.2f}, MACD: {macd:.4f}")
            
            # Sell signal: RSI overbought + MACD bearish
            elif rsi and rsi > self.rsi_overbought and macd and signal:
                if macd < signal and histogram < 0:
                    signal_result = {'action': 'SELL', 'strength': 0.8}
                    logger.info(f"SELL signal generated - RSI: {rsi:.2f}, MACD: {macd:.4f}")
            
            return signal_result
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return {'action': 'HOLD', 'strength': 0}
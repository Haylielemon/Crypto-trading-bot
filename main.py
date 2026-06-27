#!/usr/bin/env python3
"""
Crypto Trading Bot - Main Entry Point

Usage:
    python main.py
"""

import sys
import os
from bot import AutoTradingBot
from logger import setup_logger

logger = setup_logger()

def main():
    """
    Main function to start the trading bot
    """
    try:
        # Initialize bot
        bot = AutoTradingBot()
        
        # Run bot (update interval in seconds)
        # 60 seconds = 1 minute checks
        bot.run(interval=60)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
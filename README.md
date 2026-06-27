# Crypto Trading Bot - Binance Automated Trading

An automated cryptocurrency trading bot that trades on Binance with intelligent strategy, risk management, and real-time monitoring.

## Features

- ✅ **Automated Trading**: Buy/Sell signals based on technical indicators
- ✅ **Risk Management**: Stop-loss, take-profit, position sizing
- ✅ **Technical Analysis**: RSI, MACD, SMA indicators
- ✅ **Real-time Monitoring**: Live balance and trade tracking
- ✅ **Leverage Trading**: Configurable leverage support
- ✅ **Logging**: Comprehensive trade and error logs
- ✅ **Goal Tracking**: Target profit and deadline management

## Prerequisites

- Python 3.8+
- Binance API credentials (API Key and Secret)
- $50+ initial capital

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Haylielemon/Crypto-trading-bot.git
   cd Crypto-trading-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API credentials**
   ```bash
   cp .env.example .env
   # Edit .env with your Binance API credentials
   ```

## Setup Binance API

1. Go to [Binance API Management](https://www.binance.com/en/account/api-management)
2. Create a new API Key
3. Enable Spot Trading and Margin Trading (if using leverage)
4. Copy your API Key and Secret to `.env`

## Configuration

Edit `.env` file to customize:

```env
# Trading Parameters
TRADING_PAIR=BTCUSDT          # Trading pair
INITIAL_BALANCE=50             # Starting balance ($)
TARGET_PROFIT=5000            # Target profit ($)
DEADLINE_DAYS=14              # Deadline (days)

# Risk Management
MAX_LOSS_PERCENT=10           # Max loss % of balance
TAKE_PROFIT_PERCENT=20        # Take profit %
STOP_LOSS_PERCENT=5           # Stop loss %
LEVERAGE=2                    # Trading leverage

# Strategy Parameters
RSI_PERIOD=14                 # RSI period
RSI_OVERBOUGHT=70             # RSI overbought level
RSI_OVERSOLD=30               # RSI oversold level
```

## Usage

### Run the bot
```bash
python main.py
```

The bot will:
1. Connect to Binance API
2. Analyze price data every 60 seconds
3. Generate buy/sell signals based on indicators
4. Execute trades automatically
5. Manage stop-loss and take-profit
6. Track progress toward target

### View logs
```bash
ls -la logs/
tail -f logs/trading_bot_*.log
```

## Trading Strategy

The bot uses a combination of indicators:

### Buy Signal
- RSI < 30 (Oversold)
- MACD crosses above signal line
- Price below 20-day SMA

### Sell Signal
- RSI > 70 (Overbought)
- MACD crosses below signal line
- Price above 20-day SMA

### Exit Conditions
- Stop Loss: Entry price - 5%
- Take Profit: Entry price + 20%
- Deadline: Bot stops after 14 days
- Target Reached: Bot stops after $5000 profit

## Risk Management

- **Position Sizing**: Automatically calculated based on risk
- **Leverage**: Configurable (default: 2x)
- **Max Loss**: Bot stops if losses exceed 10% of balance
- **Margin**: Uses your Binance margin wallet

## Project Structure

```
.
├── main.py                 # Entry point
├── bot.py                  # Main bot logic
├── binance_client.py       # Binance API wrapper
├── strategy.py             # Trading strategy & indicators
├── risk_manager.py         # Risk management
├── config.py               # Configuration
├── logger.py               # Logging setup
├── requirements.txt        # Dependencies
├── .env.example            # Environment variables template
└── README.md              # This file
```

## Important Notes

⚠️ **WARNING**: 
- Trading cryptocurrency is risky
- Past performance ≠ future results
- Always start with small amounts
- Test with testnet before live trading
- Never share API keys or secrets
- Keep API keys with minimal permissions

## Security

1. **Never** commit `.env` file to git
2. Use **read-only** API keys if possible
3. Enable **IP Whitelist** on Binance
4. **Monitor** account activity regularly
5. Use **Stop Loss** to limit losses

## Troubleshooting

### API Connection Error
- Check API credentials in `.env`
- Verify IP is whitelisted on Binance
- Check internet connection

### Order Placement Error
- Verify account has sufficient balance
- Check trading pair symbol is correct
- Ensure minimum order quantity is met

### Strategy Not Working
- Check market conditions
- Verify indicator parameters
- Review logs for signals
- Consider adjusting strategy parameters

## Support & Documentation

- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [python-binance](https://python-binance.readthedocs.io/)
- [Technical Analysis Library](https://github.com/bukosabino/ta)

## License

MIT License

## Disclaimer

This bot is provided as-is for educational purposes. The authors are not responsible for any financial losses. Use at your own risk.

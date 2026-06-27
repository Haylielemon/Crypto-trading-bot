# 🚀 Quick Start Setup Guide

## Step 1: Get Binance API Keys (5 minutes)

1. **Create Binance Account** (if you don't have one)
   - Go to https://www.binance.com
   - Sign up with email
   - Complete 2FA setup

2. **Generate API Keys**
   - Login to Binance
   - Go to Account (icon) → API Management
   - Click "Create API"
   - Label: "Trading Bot"
   - Confirm with email
   - Copy API Key
   - Copy Secret Key

3. **Save Keys Securely**
   - Open `.env` file in this project
   - Paste API Key next to `BINANCE_API_KEY=`
   - Paste Secret Key next to `BINANCE_SECRET_KEY=`
   - **NEVER** commit `.env` to Git

## Step 2: Fund Your Account (2 minutes)

1. Go to Binance → Wallet → Deposit
2. Select USD or your preferred currency
3. Transfer $50-$100 to Binance
4. Wait for deposit to confirm

## Step 3: Configure Bot Settings (3 minutes)

Edit `.env` file with your preferences:

```env
# For aggressive (riskier) trading:
LEVERAGE=10
MAX_RISK_PER_TRADE=0.05

# For moderate trading:
LEVERAGE=5
MAX_RISK_PER_TRADE=0.03

# For conservative trading:
LEVERAGE=3
MAX_RISK_PER_TRADE=0.02
```

## Step 4: Install & Run (5 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Test connection
python -c "from binance_client import BinanceClientWrapper; client = BinanceClientWrapper(); print(client.get_account_balance())"

# Start bot
python trading_bot.py
```

## Step 5: Monitor & Adjust

Watch `bot.log` for trades and adjust settings as needed.

## Common Issues & Fixes

### "API Key Invalid"
- ✅ Copy the full key (all characters)
- ✅ Check for extra spaces
- ✅ Verify in `.env` file

### "Account has insufficient balance"
- ✅ Add more funds to Binance
- ✅ Wait for deposit confirmation
- ✅ Check account balance on Binance website

### "No buy signals"
- ✅ Market may be consolidating
- ✅ Try different timeframe
- ✅ Check market volatility

### Bot won't start
- ✅ Ensure Python 3.8+: `python --version`
- ✅ Virtual environment activated
- ✅ Dependencies installed: `pip install -r requirements.txt`

## Next Steps

1. ✅ Run bot in test mode (signals only, no real trades)
2. ✅ Monitor for 24-48 hours
3. ✅ Verify strategy works
4. ✅ Uncomment trade execution in `trading_bot.py`
5. ✅ Start live trading with caution

## Safety Checklist

- [ ] API keys added to `.env`
- [ ] `.env` added to `.gitignore`
- [ ] Binance account funded
- [ ] Account 2FA enabled
- [ ] Bot tested in signal-only mode
- [ ] Stop loss configured
- [ ] Risk limits set
- [ ] Discord alerts working (optional)

---

**Ready to trade? 🚀 Start with `python trading_bot.py`**

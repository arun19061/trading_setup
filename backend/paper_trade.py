import yfinance as yf
import datetime
import pandas as pd
import os

SYMBOL = "RELIANCE.NS"
TRADE_LOG = "/mnt/data/trading_setup/backend/trade_log.csv"

cash = 100000
position = 0
buy_price = 0
in_position = False

def simulate_trade():
    global cash, position, buy_price, in_position
    df = yf.download(SYMBOL, period="5d", interval="1m", progress=False)
    df['SMA20'] = df['Close'].rolling(20).mean()
    df['SMA50'] = df['Close'].rolling(50).mean()
    latest = df.iloc[-1]
    current_price = latest['Close']
    sma20 = latest['SMA20']
    sma50 = latest['SMA50']
    now = datetime.datetime.now()

    if not in_position and sma20 > sma50:
        quantity = cash / current_price
        buy_price = current_price
        position = quantity
        cash = 0
        in_position = True
        log_trade("BUY", current_price, quantity, cash, now)
    elif in_position and sma20 < sma50:
        cash = position * current_price
        log_trade("SELL", current_price, position, cash, now)
        position = 0
        in_position = False

def log_trade(action, price, qty, cash_bal, timestamp):
    with open(TRADE_LOG, "a") as f:
        f.write(f"{timestamp},{action},{price},{qty},{cash_bal}\n")

def get_portfolio():
    return {
        "cash": cash,
        "position": position,
        "in_position": in_position,
        "symbol": SYMBOL
    }

def get_logs():
    if not os.path.exists(TRADE_LOG):
        return []
    df = pd.read_csv(TRADE_LOG, names=["timestamp", "action", "price", "quantity", "cash_balance"])
    return df.to_dict(orient="records")

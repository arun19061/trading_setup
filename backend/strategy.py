import yfinance as yf

def run_strategy(symbol):
    data = yf.download(symbol, period="6mo", interval="1d")
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['Signal'] = 0
    data['Signal'][data['SMA20'] > data['SMA50']] = 1
    data['Signal'][data['SMA20'] < data['SMA50']] = -1
    return {
        "dates": list(data.index.strftime("%Y-%m-%d")),
        "close": list(data['Close']),
        "sma20": list(data['SMA20']),
        "sma50": list(data['SMA50']),
        "signal": list(data['Signal']),
    }

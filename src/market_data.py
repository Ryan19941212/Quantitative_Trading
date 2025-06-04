"""Market data utilities for fetching real-time prices."""

import ccxt


def fetch_current_price(symbol="BTC/USDT", exchange="binance"):
    """Return the latest price for the given symbol using ccxt."""
    ex = getattr(ccxt, exchange)()
    ticker = ex.fetch_ticker(symbol)
    return ticker["last"]

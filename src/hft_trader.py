"""High Frequency Trading example using ccxt.
This script fetches real-time price data from a cryptocurrency exchange
and applies a simple mean reversion strategy. It demonstrates how to
automatically adjust trading decisions based on live market prices.

Disclaimer: This is a simplified educational example and should not be
used for real trading without extensive testing. The authors are not
responsible for any financial loss.
"""

import asyncio
from datetime import datetime
import pandas as pd
import ccxt.async_support as ccxt

from strategies.mean_reversion import mean_reversion_strategy

class HFTTrader:
    def __init__(self, symbol="BTC/USDT", exchange="binance", window=3):
        self.exchange = getattr(ccxt, exchange)()
        self.symbol = symbol
        self.window = window
        self.data = pd.DataFrame(columns=["timestamp", "close"])

    async def fetch_price(self):
        ticker = await self.exchange.fetch_ticker(self.symbol)
        return ticker["last"], ticker["datetime"]

    async def trade_loop(self, interval=1.0):
        try:
            while True:
                price, ts = await self.fetch_price()
                self.data.loc[len(self.data)] = [ts, price]
                recent = self.data.tail(self.window).copy()
                df_signal = mean_reversion_strategy(recent, window=self.window)
                signal = df_signal["signals"].iloc[-1]
                print(f"{ts} price={price:.2f} signal={signal}")
                # Here you would place real orders based on `signal`
                await asyncio.sleep(interval)
        finally:
            await self.exchange.close()


def main():
    trader = HFTTrader()
    asyncio.run(trader.trade_loop())


if __name__ == "__main__":
    main()

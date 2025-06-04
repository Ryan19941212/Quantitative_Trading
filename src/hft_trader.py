"""High-frequency trading example with AI-assisted signals.
The trader streams market prices from an exchange and generates
signals using both a mean reversion strategy and a simple AI model."""

import asyncio
import pandas as pd
import ccxt.async_support as ccxt

from strategies.mean_reversion import mean_reversion_strategy
from ai_predictor import AIPredictor
from strategy_recommender import StrategyRecommender

class HFTTrader:
    def __init__(self, symbol="BTC/USDT", exchange="binance", window=3):
        self.exchange = getattr(ccxt, exchange)()
        self.symbol = symbol
        self.window = window
        self.data = pd.DataFrame(columns=["timestamp", "close"])
        self.ai = AIPredictor()
        self.recommender = StrategyRecommender()

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
                pred = self.ai.predict_next_close(self.data)
                recommendation = self.recommender.recommend(self.data, ai_pred=pred)
                pred_disp = f"{pred:.2f}" if pred else "N/A"
                print(
                    f"{ts} price={price:.2f} pred={pred_disp} "
                    f"signal={signal} action={recommendation}"
                )
                # Here you would place real orders based on `signal`
                await asyncio.sleep(interval)
        finally:
            await self.exchange.close()


def main():
    trader = HFTTrader()
    asyncio.run(trader.trade_loop())


if __name__ == "__main__":
    main()

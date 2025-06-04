print("Hello Quant Trading!")

import datetime
from ai_predictor import AIPredictor
from strategy_recommender import StrategyRecommender
from strategies.mean_reversion import mean_reversion_strategy
from backtest.backtester import simple_backtest

if __name__ == "__main__":
    try:
        from data.data_loader import fetch_yahoo_stock
        today = datetime.date.today()
        one_month_ago = today - datetime.timedelta(days=30)
        df_nvda = fetch_yahoo_stock("NVDA", start=one_month_ago.strftime("%Y-%m-%d"))
        df_nvda = df_nvda.dropna(subset=['close'])
        df_nvda_with_signals = mean_reversion_strategy(df_nvda)
        df_nvda_bt = simple_backtest(df_nvda_with_signals)
        ai = AIPredictor()
        pred_price = ai.predict_next_close(df_nvda)
        if pred_price:
            print(f"AI預測NVDA明日收盤價: {pred_price:.2f}")
        else:
            print("資料不足，無法預測")
        recommender = StrategyRecommender()
        recommended = recommender.recommend(df_nvda, ai_pred=pred_price)
        print(f"AI推薦策略: {recommended}")
    except Exception as e:
        print(f"yfinance 下載或回測失敗: {e}")
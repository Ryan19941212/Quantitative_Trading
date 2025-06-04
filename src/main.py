print("Hello Quant Trading!")

import datetime
from ai_predictor import AIPredictor
from strategy_recommender import StrategyRecommender
from strategies.mean_reversion import mean_reversion_strategy
from backtest.backtester import simple_backtest
from data.data_loader import fetch_yahoo_stock


def get_nvda_data():
    today = datetime.date.today()
    one_month_ago = today - datetime.timedelta(days=30)
    return fetch_yahoo_stock("NVDA", start=one_month_ago.strftime("%Y-%m-%d")).dropna(subset=['close'])


def main():
    try:
        df_nvda = get_nvda_data()
        df_nvda = mean_reversion_strategy(df_nvda)
        simple_backtest(df_nvda)
        ai = AIPredictor()
        pred_price = ai.predict_next_close(df_nvda)
        recommender = StrategyRecommender()
        print(f"AI預測NVDA明日收盤價: {pred_price:.2f}" if pred_price else "資料不足，無法預測")
        rec_result = recommender.recommend(df_nvda, ai_pred=pred_price)
        print(f"AI推薦策略: {rec_result['strategy']}")
        print(f"決策依據: 現價={rec_result['last_close']}, AI預測={rec_result['ai_pred']}, 判斷式={rec_result['decision']}")
    except Exception as e:
        print(f"yfinance 下載或回測失敗: {e}")

if __name__ == "__main__":
    main()
print("Hello Quant Trading!")

import datetime
from ai_predictor import AIPredictor
from strategy_recommender import StrategyRecommender
from strategies.mean_reversion import mean_reversion_strategy
from backtest.backtester import simple_backtest
from data.data_loader import fetch_yahoo_stock


def get_stock_data(symbol, years=5):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=365*years)
    return fetch_yahoo_stock(symbol, start=start_date.strftime("%Y-%m-%d")).dropna(subset=['close'])


def main():
    try:
        symbol = input("請輸入股票代碼（如 NVDA）：").strip().upper()
        df = get_stock_data(symbol)
        df = mean_reversion_strategy(df)
        simple_backtest(df)
        ai = AIPredictor()
        pred_1d, pred_5d, pred_22d = ai.predict_multi_horizon(df)
        print(f"AI預測{symbol}明日收盤價: {pred_1d:.2f}" if pred_1d else "資料不足，無法預測明日價")
        print(f"AI預測{symbol}一週後收盤價: {pred_5d:.2f}" if pred_5d else "資料不足，無法預測一週價")
        print(f"AI預測{symbol}一個月後收盤價: {pred_22d:.2f}" if pred_22d else "資料不足，無法預測一個月價")
        recommender = StrategyRecommender()
        rec_result = recommender.recommend(df, ai_pred=pred_1d)
        print(f"AI推薦策略: {rec_result['strategy']}")
        last_close = rec_result['last_close']
        ai_pred = rec_result['ai_pred']
        if last_close is not None and ai_pred is not None:
            print(f"決策依據: 現價={last_close:.2f}, AI預測={ai_pred:.2f}")
        else:
            print(f"決策依據: 現價={last_close}, AI預測={ai_pred}")
    except Exception as e:
        print(f"yfinance 下載或回測失敗: {e}")

if __name__ == "__main__":
    main()
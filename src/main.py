print("Hello Quant Trading!")

import datetime
from recommender.strategy_recommender import StrategyRecommender
from data.data_loader import fetch_yahoo_stock
from ai.rl_trader import QLearningTrader
from strategies.mean_reversion import mean_reversion_strategy
from backtest.backtester import simple_backtest


def get_stock_data(symbol, years=5):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=365*years)
    return fetch_yahoo_stock(symbol, start=start_date.strftime("%Y-%m-%d")).dropna(subset=['close'])


def main():
    try:
        symbol = input("請輸入股票代碼（如 NVDA）：").strip().upper()
        df = get_stock_data(symbol)
        print("\n強化學習 Q-Learning 交易建議：")
        rl_agent = QLearningTrader()
        rl_agent.train(df, n_episodes=100)
        closes = df['close'].values
        min_price, max_price = closes.min(), closes.max()
        position = 0
        cash = 100000
        stock = 0
        # 顯示未來一天的Q-Learning建議
        next_state = rl_agent._discretize(closes[-1], min_price, max_price)
        next_action = rl_agent.q_table[next_state].argmax()
        if next_action == 1 and position == 0:
            print(f"Q-Learning 建議明天買進，參考價格={closes[-1]:.2f}")
        elif next_action == 2 and position == 1:
            print(f"Q-Learning 建議明天賣出，參考價格={closes[-1]:.2f}")
        else:
            print(f"Q-Learning 建議明天持有/不動作，參考價格={closes[-1]:.2f}")
        print("Q-Learning 建議操作已顯示完畢。")
    except Exception as e:
        print(f"yfinance 下載或回測失敗: {e}")

if __name__ == "__main__":
    main()
import pandas as pd

def simple_backtest(df, initial_cash=100000):
    """
    根據 signals 欄位進行簡單回測：
    - 1: 全部資金買進
    - -1: 全部賣出（持有現金）
    - 0: 無動作，維持前一狀態
    回傳 DataFrame，包含資產淨值（equity）
    """
    df = df.copy()
    position = 0  # 0: 空手, 1: 持有
    cash = initial_cash
    equity_list = []
    last_price = None
    for idx, row in df.iterrows():
        signal = row.get('signals', 0)
        price = row['close']
        if signal == 1 and position == 0:
            # 全部資金買進
            position = cash / price
            cash = 0
        elif signal == -1 and position > 0:
            # 全部賣出
            cash = position * price
            position = 0
        # 計算當前資產淨值
        equity = cash + (position * price if position > 0 else 0)
        equity_list.append(equity)
        last_price = price
    df['equity'] = equity_list
    return df

import pandas as pd

def mean_reversion_strategy(df, window=3):
    """
    簡單均值回歸策略：
    當收盤價低於移動平均線時買進，高於移動平均線時賣出。
    回傳一個 signals 欄位：1=買進, -1=賣出, 0=無動作
    """
    df = df.copy()
    df['ma'] = df['close'].rolling(window=window).mean()
    df['signals'] = 0
    df.loc[df['close'] < df['ma'], 'signals'] = 1
    df.loc[df['close'] > df['ma'], 'signals'] = -1
    return df

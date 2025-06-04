import yfinance as yf
import pandas as pd

def fetch_yahoo_stock(symbol, start="2023-01-01", end=None):
    """
    從 Yahoo Finance 下載股票資料
    symbol: 股票代碼（如 'NVDA'）
    start, end: 日期範圍
    回傳 DataFrame
    """
    df = yf.download(symbol, start=start, end=end)
    df = df.reset_index()
    # 攤平 MultiIndex 欄位，並全部轉小寫
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0].lower() for col in df.columns]
    else:
        df.columns = [col.lower() for col in df.columns]
    return df

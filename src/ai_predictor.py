"""
ai_predictor.py
簡易AI預測模組：用線性回歸預測未來一天收盤價
"""
import numpy as np
from sklearn.linear_model import LinearRegression

class AIPredictor:
    def predict_next_close(self, df):
        # 假設 df 有 'close' 欄位，取最近20天做預測
        if len(df) < 20:
            return None
        closes = df['close'].values[-20:]
        X = np.arange(20).reshape(-1, 1)
        y = closes
        model = LinearRegression().fit(X, y)
        next_day = np.array([[20]])
        pred = model.predict(next_day)[0]
        return float(pred)

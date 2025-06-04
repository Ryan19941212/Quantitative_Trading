"""
ai_predictor.py
簡易AI預測模組：用線性回歸預測未來一天/一週/一個月收盤價
"""
import numpy as np
from sklearn.linear_model import LinearRegression

class AIPredictor:
    def predict_next_close(self, df):
        # 舊方法，預測明天
        if len(df) < 20:
            return None
        closes = df['close'].values[-20:]
        X = np.arange(20).reshape(-1, 1)
        y = closes
        model = LinearRegression().fit(X, y)
        next_day = np.array([[20]])
        pred = model.predict(next_day)[0]
        return float(pred)

    def predict_multi_horizon(self, df):
        """
        預測明天(1d)、一週(5d)、一個月(22d)後的收盤價
        """
        if len(df) < 20:
            return None, None, None
        closes = df['close'].values[-20:]
        X = np.arange(20).reshape(-1, 1)
        y = closes
        model = LinearRegression().fit(X, y)
        pred_1d = float(model.predict(np.array([[20]]))[0])
        pred_5d = float(model.predict(np.array([[24]]))[0])  # 20+4=24
        pred_22d = float(model.predict(np.array([[41]]))[0]) # 20+21=41
        return pred_1d, pred_5d, pred_22d

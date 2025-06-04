"""
ai_predictor.py
多模型預測：線性回歸、隨機森林
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

class AIPredictor:
    def predict_next_close(self, df):
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
        if len(df) < 20:
            return None, None, None
        closes = df['close'].values[-20:]
        X = np.arange(20).reshape(-1, 1)
        y = closes
        model = LinearRegression().fit(X, y)
        pred_1d = float(model.predict(np.array([[20]]))[0])
        pred_5d = float(model.predict(np.array([[24]]))[0])
        pred_22d = float(model.predict(np.array([[41]]))[0])
        return pred_1d, pred_5d, pred_22d

    def predict_multi_model(self, df):
        """
        回傳 dict: {model_name: (明天, 一週, 一個月)}
        """
        if len(df) < 20:
            return {}
        closes = df['close'].values[-20:]
        X = np.arange(20).reshape(-1, 1)
        y = closes
        # 線性回歸
        lr = LinearRegression().fit(X, y)
        # 隨機森林
        rf = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)
        # 預測點
        X_pred = np.array([[20], [24], [41]])
        result = {
            'LinearRegression': tuple([float(x) for x in lr.predict(X_pred)]),
            'RandomForest': tuple([float(x) for x in rf.predict(X_pred)])
        }
        return result

"""
ai_predictor.py
只用隨機森林作為AI預測模型
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

class AIPredictor:
    def predict_next_close(self, df):
        if len(df) < 20:
            return None
        closes = df['close'].values[-20:]
        X = np.arange(20).reshape(-1, 1)
        y = closes
        model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)
        next_day = np.array([[20]])
        pred = model.predict(next_day)[0]
        return float(pred)

    def predict_multi_horizon(self, df):
        if len(df) < 20:
            return None, None, None
        closes = df['close'].values[-20:]
        X = np.arange(20).reshape(-1, 1)
        y = closes
        model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)
        pred_1d = float(model.predict(np.array([[20]]))[0])
        pred_5d = float(model.predict(np.array([[24]]))[0])
        pred_22d = float(model.predict(np.array([[41]]))[0])
        return pred_1d, pred_5d, pred_22d

    def predict_multi_model(self, df):
        # 只回傳隨機森林
        if len(df) < 20:
            return {}
        closes = df['close'].values[-20:]
        X = np.arange(20).reshape(-1, 1)
        y = closes
        model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)
        X_pred = np.array([[20], [24], [41]])
        preds = model.predict(X_pred)
        return {'RandomForest': tuple([float(x) for x in preds])}

    def backtest_models(self, df, horizon=1):
        # 只回測隨機森林
        if len(df) < 40:
            return {}
        closes = df['close'].values
        preds = []
        trues = []
        for i in range(20, len(closes) - horizon):
            X = np.arange(i-20, i).reshape(-1, 1)
            y = closes[i-20:i]
            model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)
            pred = model.predict(np.array([[i]]))[0]
            preds.append(pred)
            trues.append(closes[i + horizon])
        mse = mean_squared_error(trues, preds) if preds else None
        return {'RandomForest': mse} if mse is not None else {}

"""
ai_predictor.py
多模型預測：線性回歸、隨機森林、KNN、SVR
並可回測各模型在歷史資料上的預測誤差
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

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
        X_pred = np.array([[20], [24], [41]])
        models = {
            'LinearRegression': LinearRegression(),
            'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
            'KNN': KNeighborsRegressor(n_neighbors=3),
            'SVR': SVR()
        }
        result = {}
        for name, model in models.items():
            model.fit(X, y)
            preds = model.predict(X_pred)
            result[name] = tuple([float(x) for x in preds])
        return result

    def backtest_models(self, df, horizon=1):
        """
        回測各模型在歷史資料上的預測誤差 (MSE)
        horizon: 預測幾天後的收盤價 (1=明天, 5=一週, 22=一個月)
        回傳 dict: {model_name: mse}
        """
        if len(df) < 40:
            return {}
        closes = df['close'].values
        mses = {}
        models = {
            'LinearRegression': LinearRegression(),
            'RandomForest': RandomForestRegressor(n_estimators=100, random_state=42),
            'KNN': KNeighborsRegressor(n_neighbors=3),
            'SVR': SVR()
        }
        for name, model in models.items():
            preds = []
            trues = []
            for i in range(20, len(closes) - horizon):
                X = np.arange(i-20, i).reshape(-1, 1)
                y = closes[i-20:i]
                model.fit(X, y)
                pred = model.predict(np.array([[i]]))[0]
                preds.append(pred)
                trues.append(closes[i + horizon])
            if preds:
                mses[name] = mean_squared_error(trues, preds)
        return mses

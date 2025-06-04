"""
strategy_recommender.py
策略推薦模組（初版）
"""
class StrategyRecommender:
    def recommend(self, data, ai_pred=None):
        # 根據 AI 預測結果推薦策略
        if ai_pred is not None and len(data) > 0:
            last_close = data['close'].values[-1]
            if ai_pred > last_close * 1.01:
                return ["buy", "mean_reversion"]
            elif ai_pred < last_close * 0.99:
                return ["sell", "mean_reversion"]
            else:
                return ["hold", "mean_reversion"]
        # 沒有 AI 預測時，回傳預設策略
        return ["mean_reversion"]

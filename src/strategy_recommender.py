"""
strategy_recommender.py
策略推薦模組（初版）
"""
from recommender.strategy_recommender import StrategyRecommender

class StrategyRecommender:
    def recommend(self, data, ai_pred=None):
        # 根據 AI 預測結果推薦策略，並回傳決策依據
        result = {
            'strategy': None,
            'decision': None,
            'last_close': None,
            'ai_pred': ai_pred
        }
        if ai_pred is not None and len(data) > 0:
            last_close = data['close'].values[-1]
            result['last_close'] = float(last_close)
            if ai_pred > last_close * 1.01:
                result['strategy'] = ['buy', 'mean_reversion']
                result['decision'] = 'ai_pred > last_close * 1.01'
            elif ai_pred < last_close * 0.99:
                result['strategy'] = ['sell', 'mean_reversion']
                result['decision'] = 'ai_pred < last_close * 0.99'
            else:
                result['strategy'] = ['hold', 'mean_reversion']
                result['decision'] = '其他情況'
        else:
            result['strategy'] = ['mean_reversion']
            result['decision'] = '無AI預測'
        return result

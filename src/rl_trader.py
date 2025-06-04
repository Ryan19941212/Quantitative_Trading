"""
rl_trader.py
簡易 Q-Learning 強化學習交易代理人
"""
import numpy as np
import pandas as pd

class QLearningTrader:
    def __init__(self, n_states=10, n_actions=3, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.n_states = n_states  # 狀態離散化數量
        self.n_actions = n_actions  # 0:持有, 1:買, 2:賣
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((n_states, n_actions))

    def _discretize(self, price, min_price, max_price):
        # 將價格離散化為 n_states
        return int((price - min_price) / (max_price - min_price + 1e-8) * (self.n_states - 1))

    def train(self, df, n_episodes=100):
        closes = df['close'].values
        min_price, max_price = closes.min(), closes.max()
        for _ in range(n_episodes):
            position = 0  # 0:空手, 1:持有
            cash = 100000
            stock = 0
            for t in range(len(closes) - 1):
                state = self._discretize(closes[t], min_price, max_price)
                if np.random.rand() < self.epsilon:
                    action = np.random.choice(self.n_actions)
                else:
                    action = np.argmax(self.q_table[state])
                # 執行動作
                reward = 0
                if action == 1 and position == 0:  # 買
                    stock = cash / closes[t]
                    cash = 0
                    position = 1
                elif action == 2 and position == 1:  # 賣
                    cash = stock * closes[t]
                    stock = 0
                    position = 0
                # 計算 reward: 下一時刻的總資產變化
                next_state = self._discretize(closes[t+1], min_price, max_price)
                next_equity = cash + stock * closes[t+1]
                curr_equity = cash + stock * closes[t]
                reward = next_equity - curr_equity
                # Q-Learning 更新
                self.q_table[state, action] += self.alpha * (
                    reward + self.gamma * np.max(self.q_table[next_state]) - self.q_table[state, action]
                )

    def test(self, df):
        closes = df['close'].values
        min_price, max_price = closes.min(), closes.max()
        position = 0
        cash = 100000
        stock = 0
        equity_curve = []
        for t in range(len(closes)):
            state = self._discretize(closes[t], min_price, max_price)
            action = np.argmax(self.q_table[state])
            if action == 1 and position == 0:
                stock = cash / closes[t]
                cash = 0
                position = 1
            elif action == 2 and position == 1:
                cash = stock * closes[t]
                stock = 0
                position = 0
            equity = cash + stock * closes[t]
            equity_curve.append(equity)
        return equity_curve

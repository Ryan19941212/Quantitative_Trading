# 量化交易 AI 專案

本專案為量化交易自動化決策系統，支援 Q-Learning 強化學習自動給出股票操作建議。

## 專案結構

```
Qantitative trading/
├── README.md
├── requirements.txt
└── src/
    ├── main.py                  # 主程式入口
    ├── ai/                      # AI/強化學習模組
    │   ├── __init__.py
    │   └── rl_trader.py         # Q-Learning 交易代理人
    ├── strategies/              # 交易策略
    │   ├── __init__.py
    │   └── mean_reversion.py
    ├── backtest/                # 回測模組
    │   ├── __init__.py
    │   └── backtester.py
    ├── data/                    # 資料處理
    │   ├── __init__.py
    │   └── data_loader.py
    ├── recommender/             # 策略推薦
    │   ├── __init__.py
    │   └── strategy_recommender.py
    └── utils/                   # 工具/輔助模組
        └── __init__.py
```

## 執行方式
1. 安裝依賴：
   ```sh
   pip install -r requirements.txt
   ```
2. 執行主程式：
   ```sh
   python src/main.py
   ```

## 主要功能
- 支援 Q-Learning 強化學習自動學習買賣時機
- 可查詢任意股票，並根據過去五年資料給出明天操作建議
- 架構模組化，方便擴充多種 AI/策略/資料來源

## 依賴套件
- yfinance
- scikit-learn
- pandas

---
如需擴充功能或有任何問題，歡迎討論！

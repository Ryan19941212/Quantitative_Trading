# 量化交易 Side Project

這是一個用於量化交易策略開發與回測的 side project。

## 專案結構
- src/main.py：主程式進入點
- src/strategies/：放置各種交易策略
- src/data/：資料載入與處理
- src/backtest/：回測模組
- src/utils/：輔助工具
- src/hft_trader.py：高頻交易與 AI 信號示例

## 如何開始
1. 安裝依賴：`pip install -r requirements.txt`
2. 執行主程式：`python src/main.py`

## 高頻交易範例
執行 `python src/hft_trader.py` 連接交易所取得即時價格，
結合均值回歸與 AI 預測，自動產生交易信號。

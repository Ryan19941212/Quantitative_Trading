# 量化交易 Side Project

這是一個用於量化交易策略開發與回測的 side project。

## 專案結構
- src/main.py：主程式進入點
- src/strategies/：放置各種交易策略
- src/data/：資料載入與處理
- src/backtest/：回測模組
- src/utils/：輔助工具
- src/hft_trader.py：簡易高頻交易示例

## 如何開始
1. 安裝依賴：`pip install -r requirements.txt`
2. 執行主程式：`python src/main.py`

## 高頻交易範例
執行 `python src/hft_trader.py` 可連接至交易所取得即時價格，
運行均值回歸策略並輸出交易信號。此範例僅供學術研究，
不建議直接用於實盤交易。

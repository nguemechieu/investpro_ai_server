╭────────────────────────────────────────────────────────────╮
│                                                            │
│        🖥️ Java Client (InvestPro CandleStickChart)         │
│                                                            │
│  - Collects real-time Candle Data                          │
│  - Extracts Features (EMA, RSI, MACD, etc.)                │
│  - Sends features via HTTP POST to FastAPI server          │
│  - Receives prediction ("up"/"down" + confidence)          │
│  - Feeds prediction into AI PaperTradingBot                │
│                                                            │
╰────────────────────────────────────────────────────────────╯
|
| JSON HTTP POST
↓
╭────────────────────────────────────────────────────────────╮
│                                                            │
│       🚀 FastAPI Server (inside Docker Container)          │
│                                                            │
│  - Endpoint: POST /predict                                 │
│  - Receives feature vector from Java                      │
│  - Scales features (StandardScaler: investpro_scaler.pkl) │
│  - Loads trained DNN Model (investpro_ai_dnn_model.h5)     │
│  - Predicts BUY/SELL probability                          │
│  - Returns prediction + confidence                        │
│                                                            │
╰────────────────────────────────────────────────────────────╯
|
| AI Prediction Response
↓
╭────────────────────────────────────────────────────────────╮
│                                                            │
│        🧠 Java AI PaperTradingBot (InvestProAIPaperTradingBot)│
│                                                            │
│  - Opens simulated trades (paper trading)                 │
│  - Manages risk, stop-loss, take-profit                   │
│  - Tracks profit/loss and Equity Curve                    │
│  - Displays Real-Time Equity Growth Chart (JavaFX)        │
│                                                            │
╰────────────────────────────────────────────────────────────╯

![arch]("./docs/achitechture.png")
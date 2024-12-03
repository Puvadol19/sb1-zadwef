from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
from mt5_client import MT5Client
from ml_model import TradingModel
from telegram_notifier import TelegramNotifier
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
mt5_client = MT5Client()
trading_model = TradingModel("models/trading_model")
telegram_notifier = TelegramNotifier(
    token=os.getenv("TELEGRAM_BOT_TOKEN"),
    chat_id=os.getenv("TELEGRAM_CHAT_ID")
)

class TradeRequest(BaseModel):
    symbol: str
    action: str
    volume: float

@app.on_event("startup")
async def startup_event():
    mt5_client.initialize()

@app.on_event("shutdown")
async def shutdown_event():
    mt5_client.shutdown()

@app.post("/trade/")
async def trade(request: TradeRequest):
    try:
        # Get market data for prediction
        market_data = mt5_client.get_market_data(request.symbol, mt5.TIMEFRAME_M1, 10)
        
        # Get trading signal from model
        signal = trading_model.predict(market_data)
        
        # Execute trade based on signal and request
        if signal:
            order_result = mt5_client.place_order({
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": request.symbol,
                "volume": request.volume,
                "type": mt5.ORDER_BUY if request.action.lower() == "buy" else mt5.ORDER_SELL,
                "price": mt5.symbol_info_tick(request.symbol).ask
            })
            
            # Send notification
            await telegram_notifier.send_trade_notification(
                request.symbol,
                request.action,
                order_result.price,
                request.volume
            )
            
            return {"status": "success", "order": order_result._asdict()}
            
        return {"status": "rejected", "reason": "Model signal not favorable"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/market-data/{symbol}")
async def get_market_data(symbol: str):
    try:
        data = mt5_client.get_market_data(symbol, mt5.TIMEFRAME_M1, 100)
        return {"status": "success", "data": data.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
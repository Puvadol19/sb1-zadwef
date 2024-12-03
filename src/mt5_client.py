import MetaTrader5 as mt5
from typing import Dict, Any
import pandas as pd

class MT5Client:
    def __init__(self):
        self.initialized = False
        
    def initialize(self):
        if not mt5.initialize():
            raise Exception(f"Failed to initialize MT5: {mt5.last_error()}")
        self.initialized = True
        
    def shutdown(self):
        if self.initialized:
            mt5.shutdown()
            self.initialized = False
            
    def get_market_data(self, symbol: str, timeframe: int, count: int) -> pd.DataFrame:
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
        return pd.DataFrame(rates)
        
    def place_order(self, order_params: Dict[str, Any]):
        return mt5.order_send(order_params)
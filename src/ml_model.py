import mlflow
import mlflow.pyfunc
import pandas as pd
from typing import Dict, Any

class TradingModel:
    def __init__(self, model_path: str):
        self.model = mlflow.pyfunc.load_model(model_path)
        
    def predict(self, data: pd.DataFrame) -> Any:
        return self.model.predict(data)
        
    @staticmethod
    def log_model(model: Any, model_path: str):
        mlflow.pyfunc.save_model(model_path, python_model=model)
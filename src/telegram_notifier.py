from telegram import Bot
from typing import Optional

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        
    async def send_message(self, text: str) -> None:
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=text
        )
        
    async def send_trade_notification(self, 
                                    symbol: str, 
                                    action: str, 
                                    price: float, 
                                    volume: float) -> None:
        message = (
            f"Trade Executed:\n"
            f"Symbol: {symbol}\n"
            f"Action: {action}\n"
            f"Price: {price}\n"
            f"Volume: {volume}"
        )
        await self.send_message(message)
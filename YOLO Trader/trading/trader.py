import os
from alpaca_trade_api import REST
from dotenv import load_dotenv

load_dotenv()

class Trader:
    def __init__(self):
        self.api = REST(
            os.getenv('ALPACA_API_KEY'),
            os.getenv('ALPACA_SECRET_KEY'),
            os.getenv('ALPACA_BASE_URL')
        )

    def place_order(self, symbol: str, qty: int, side: str):
        return self.api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
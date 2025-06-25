import os
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DataFetcher:
    def __init__(self, symbol: str):
        self.symbol = symbol

    def fetch_historical(self, period: str = '1mo', interval: str = '1d') -> pd.DataFrame:
        data = yf.download(self.symbol, period=period, interval=interval)
        data.dropna(inplace=True)
        return data
import pandas as pd

class SMAStrategy:
    def __init__(self, short_window: int = 10, long_window: int = 50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        signals = pd.DataFrame(index=data.index)
        signals['price'] = data['Close']
        signals['short_sma'] = data['Close'].rolling(window=self.short_window).mean()
        signals['long_sma'] = data['Close'].rolling(window=self.long_window).mean()
        signals['signal'] = 0
        signals.loc[signals['short_sma'] > signals['long_sma'], 'signal'] = 1
        signals.loc[signals['short_sma'] < signals['long_sma'], 'signal'] = -1
        return signals
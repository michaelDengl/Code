from data_fetcher import DataFetcher
from strategy import SMAStrategy
from trader import Trader
import time

SYMBOL = 'AAPL'
QTY = 1
FETCH_PERIOD = '1d'
FETCH_INTERVAL = '1m'

if __name__ == '__main__':
    fetcher = DataFetcher(SYMBOL)
    strategy = SMAStrategy(short_window=5, long_window=20)
    trader = Trader()
    last_signal = 0

    while True:
        data = fetcher.fetch_historical(period=FETCH_PERIOD, interval=FETCH_INTERVAL)
        signals = strategy.generate_signals(data)
        signal = signals['signal'].iloc[-1]

        if signal == 1 and last_signal != 1:
            trader.place_order(SYMBOL, QTY, 'buy')
            print(f"Buying {QTY} shares of {SYMBOL}")
        elif signal == -1 and last_signal != -1:
            trader.place_order(SYMBOL, QTY, 'sell')
            print(f"Selling {QTY} shares of {SYMBOL}")

        last_signal = signal
        time.sleep(60)
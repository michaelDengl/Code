import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from data_fetcher import DataFetcher
from strategy import SMAStrategy

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='symbol-dropdown',
        options=[{'label': s, 'value': s} for s in ['AAPL', 'MSFT', 'TSLA']],
        value='AAPL'
    ),
    dcc.Graph(id='price-chart'),
    dcc.Interval(id='interval-component', interval=60*1000, n_intervals=0)
])

@app.callback(
    Output('price-chart', 'figure'),
    [Input('symbol-dropdown', 'value'), Input('interval-component', 'n_intervals')]
)
def update_chart(symbol, n):
    fetcher = DataFetcher(symbol)
    data = fetcher.fetch_historical(period='7d', interval='5m')
    strat = SMAStrategy(short_window=10, long_window=30)
    signals = strat.generate_signals(data)

    fig = {
        'data': [
            {'x': signals.index, 'y': signals['price'], 'type': 'line', 'name': 'Price'},
            {'x': signals.index, 'y': signals['short_sma'], 'type': 'line', 'name': 'Short SMA'},
            {'x': signals.index, 'y': signals['long_sma'], 'type': 'line', 'name': 'Long SMA'}
        ],
        'layout': {'title': f'{symbol} Price & SMA Signals'}
    }
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
import calendar
import datetime

import dash
import pandas as pd
import pandas_datareader.data as web
import plotly.graph_objects as go
from dash import dcc
from dash import html, Output, Input
from plotly.subplots import make_subplots


def generate_start_dates(start_date, end_date):
    return [{'label': calendar.month_name[d.month], 'value': d.strftime('%Y-%m-%d')}
            for d in pd.date_range(start_date, end_date, freq='1M') - pd.offsets.MonthBegin(1)]


def generate_end_dates(start_date, end_date):
    return [{'label': calendar.month_name[d.month], 'value': d.strftime('%Y-%m-%d')}
            for d in pd.date_range(start_date, end_date, freq='1M')]


app = dash.Dash(__name__)

start = datetime.datetime(2021, 1, 1)
# end = datetime.datetime(2021, 12, 31)
end = datetime.date.today()
spy = web.DataReader(['sp500'], 'fred', start, end).dropna()
btc = web.get_data_yahoo(['BTC-USD'], start, end)['Close']


@app.callback(
    Output(component_id='series-graph', component_property='figure'),
    Output(component_id='series-correlation', component_property='children'),
    Input(component_id='start-dropdown', component_property='value'),
    Input(component_id='end-dropdown', component_property='value')
)
def generate_chart(start_date, end_date):
    spy_sub = spy[start_date: end_date]
    btc_sub = btc[start_date: end_date]

    figure = make_subplots(specs=[[{"secondary_y": True}]])
    figure.add_trace(
        go.Scatter(x=spy_sub['sp500'].keys(), y=spy_sub['sp500'].values, name="S&P500"),
        secondary_y=False,
    )
    figure.add_trace(
        go.Scatter(x=btc_sub['BTC-USD'].keys(), y=btc_sub['BTC-USD'].values, name="BTCUSD"),
        secondary_y=True,
    )
    return figure, "{:.5f}".format(spy_sub.corrwith(btc_sub['BTC-USD'])[0])


# fig = generate_chart(start, end)

app.layout = html.Div(children=[
    html.H1(children='Market Correlation Sheet'),

    html.Div(children='''
        Dash: Pick two securities and time period
    '''),

    html.Div(children=[
        dcc.Dropdown(
            id='start-dropdown',
            options=generate_start_dates(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')),
            value=start.strftime('%Y-%m-%d')
        ),

        dcc.Dropdown(
            id='end-dropdown',
            options=generate_end_dates(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')),
            value=end.strftime('%Y-%m-%d')
        ),
    ]),

    # dcc.Dropdown(
    #     options=[
    #         {'label': 'S&P 500', 'value': 'spy'},
    #         {'label': 'Bitcoin', 'value': 'BTC-USD'},
    #     ],
    #     value=['spy'],
    # ),

    dcc.Graph(id='series-graph'),

    html.Br(),

    html.Label('Correlation'),
    html.Div(id='series-correlation'),
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8060)

import datetime
import pandas as pd
import dash
import pandas_datareader.data as web
import plotly.express as px
import plotly.graph_objects as go
from dash import html, Output, Input
from dash import dcc
from plotly.subplots import make_subplots


start = datetime.datetime(2021, 1, 2)
end = datetime.datetime(2021, 12, 31)
spy = web.DataReader(['sp500'], 'fred', start, end)
btc = web.get_data_yahoo(['BTC-USD'], start, end)['Close']
both = pd.concat([spy, btc], axis=1).dropna(how='any', axis=0)

app = dash.Dash(__name__)

fig = px.line(both, y=both.columns)

fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(
    go.Scatter(x=spy['sp500'].keys(), y=spy['sp500'].values, name="yaxis data"),
    secondary_y=False,
)
fig2.add_trace(
    go.Scatter(x=btc['BTC-USD'].keys(), y=btc['BTC-USD'].values, name="yaxis data"),
    secondary_y=True,
)


app.layout = html.Div(children=[
    html.H1(children='Market Correlation Sheet'),

    html.Div(children='''
        Dash: Pick two securities and time period
    '''),

    html.Div([
       "Input: ",
       dcc.Input(id='my-input', value='initial value', type='text')
    ]),

    html.Br(),

    html.Div(id='my-output'),

    dcc.Dropdown(
        options=[
            {'label': 'S&P 500', 'value': 'spy'},
            {'label': 'Bitcoin', 'value': 'BTC-USD'},
        ],
        value=['spy'],
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig2
    )
])


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True, port=8060)

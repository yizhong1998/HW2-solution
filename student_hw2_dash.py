import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output, State
import pandas as pd
from os import listdir, remove
import pickle
from time import sleep
import json




# Make a Dash app!
app = dash.Dash(__name__)

# Define the layout.
app.layout = html.Div([

    html.Br(),
    # Section title
    html.H1("Section 1: Trading strategy and parameters"),
    html.H2('Data Note & Disclaimer'),
    html.P(
        'This Dash app makes use of IBKR\'s Python API to acquire ' + \
        'the historical data for trading. These initial data ' + \
        'files were compiled using paper or demo account, which is ' + \
        'only for study usage or publicly available ' + \
        'from IBKR. This app does NOT need a IBKR ' + \
        'subscription to work -- only to update data. Always know and ' + \
        'obey your data stewardship obligations!'
    ),
    html.H2('Description of strategy'),
    html.P('This app explores a simple strategy that works as follows:'),
    html.Ul([
    html.P("1. For every day in the back test period, we run an OLS model with 90-day lookback period for the spread between IVV and DOW."),
    html.P('2. With the residuals in the previous OLS, calculate a normalized z score with standard deviation and mean, which is the Buy-Sell signal for our trade.'),
    html.P('3. With the slope of every OLS, calculate the asset weight named hedge ratio.'),
    html.P('4. BUY signal: when z score > 1, we enter; SELL signal: when z score <0.6, we exit.'),
    html.P('5. When BUY signal occurs, we use the DYNAMIC asset weight to set our holding; When SELL signal occurs, we liquidate our holding.')
            ]),
    html.H2('Parameters and button'),
    html.Div(id='trade-output'),
    # Text input for the currency pair to be traded
    # Numeric input for the trade amount
    html.Label('    backtest'),
    dcc.Input(id='backtest', type='text'),

    html.Label('    startdate'),
    dcc.Input(id = 'startdate', type = 'text'),

    html.Label('    enddate'),
    dcc.Input(id = 'enddate', type = 'text'),

    html.Label('    accountequity'),
    dcc.Input(id = 'accountequity', type = 'number'),

    html.Button('Go Live!', id='trade_submit', n_clicks=0),

    html.Br(),
    html.H1('Section 2: Plot Z-score and hedge ratio'),
    html.Div([

        dcc.Graph(id='graph_zscore')
    ]),
    html.Div([
        # Candlestick graph goes here:

        dcc.Graph(id='hedge_ratio')
    ]),

    html.Br(),
    html.H1('Section 3: Trading Blotter & Ledger'),
    html.Div([
        dcc.Graph(id = 'table')
    ])

])


# Callback for what to do when trade-button is pressed
@app.callback(
    [Output('graph_zscore', 'figure'), Output('hedge_ratio', 'figure'), Output('trade-output', 'children'),
     Output('table', 'figure')],
    [Input('trade_submit', 'n_clicks')],
    [State('backtest', 'value'), State('startdate', 'value'), State('enddate', 'value'),
     State('accountequity', 'value')],
    # We DON'T want to start executing trades just because n_clicks was initialized to 0!!!
    prevent_initial_call=True
)
def trade(n_clicks, backtest, startdate, enddate, accountequity): # Still don't use n_clicks, but we need the dependency
    msg = 'from '+ str(startdate) + ' to ' + str(enddate) + ', rolling window '+ backtest + ', trading volum ' + str(accountequity)
    # Make the message that we want to send back to trade-output
    trade_order = {
        "startdate": startdate,
        "lookback_period": backtest,
        "AccountEquity": accountequity,
        "enddate": enddate
    }
    js = json.dumps(trade_order)
    file = open('rolling_window.txt', 'w')
    #filee = open('live_trade.txt', 'w')
    file.write(js)
    #filee.write(js)
    file.close()
    #filee.close()

    while 'z_score.csv' not in listdir():
        sleep(0.1)
    df = pd.read_csv('z_score.csv')
    remove('z_score.csv')
    df['Date'] = pd.to_datetime(df['Date'].astype('string'))
    date = df['Date']
    zscore = df['z_score']
    while 'hedge_ratio.csv' not in listdir():
        sleep(0.1)
    dff = pd.read_csv('hedge_ratio.csv')
    remove('hedge_ratio.csv')
    dff['Date'] = pd.to_datetime(dff['Date'].astype('string'))
    datee = dff['Date']
    hedge_ratio = dff['hedge_ratio']

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=date, y=zscore,
                             mode='lines',
                             name='Z-score'))
    fig1.update_layout(title='Z-score')
    fig1.update_yaxes(title_text="value")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=datee, y=hedge_ratio,
                             mode='lines',
                             name='hedge ratio'))
    fig2.update_layout(title='hedge ratio')
    fig2.update_yaxes(title_text="slope")

    dft = pd.read_csv('trade_blotter.csv')
    remove('trade_blotter.csv')
    dft['Date'] = pd.to_datetime(dft['Date'].astype('string'))
    fig3 = go.Figure(data=[go.Table(
        header=dict(values=list(dft.columns)[1:],),
        cells=dict(values=[dft.Date, dft.IVV_Order, dft.IVV_Price, dft.IVV_Position, dft.DOW_Order,
                           dft.DOW_Price, dft.DOW_Position, dft.Account_Equity, dft.Asset],))
    ])

    # Dump trade_order as a pickle object to a file connection opened with write-in-binary ("wb") permission:

    # Return the message, which goes to the trade-output div's "children" attribute.
    return fig1, fig2, msg, fig3

# Run it!
if __name__ == '__main__':
    app.run_server(debug=True)

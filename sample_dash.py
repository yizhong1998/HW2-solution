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

from helper_functions import * # this statement imports all functions from your helper_functions file!

# Run your helper function to clear out any io files left over from old runs
check_for_and_del_io_files()


# Make a Dash app!
app = dash.Dash(__name__)

# Define the layout.
app.layout = html.Div([


    # Currency pair text input, within its own div.
    # html.Div(
    #     [
    #         "Input Currency: ",
    #         # Your text input object goes here:
    #         dcc.Input(id = 'currency-pair', value = 'AUDCAD',  type = 'text')
    #
    #     ],
    #     # Style it so that the submit button appears beside the input.
    #     style={'display': 'inline-block'}
    # ),

    # Line break
    # html.Br(),
    # # Div to hold the initial instructions and the updated info once submit is pressed
    # html.Div(id='output-div', children='Enter a currency code and press "submit"'),
    html.Div([
        # Candlestick graph goes here:

        dcc.Graph(id='candlestick-graph')
    ]),
    # Another line break
    html.Br(),
    # Section title
    html.H1("Z-score and trading"),
    # Div to confirm what trade was made
    html.Div(id='trade-output'),
    # Text input for the currency pair to be traded
    dcc.Input(id='window',type='text')
             ,
    # Numeric input for the trade amount
    dcc.Input(id='backtest',type='text')
             ,
    # Submit button for the trade
    html.Button('Trade', id='trade_submit', n_clicks=0)

])

# Callback for what to do when submit-button is pressed
# @app.callback(
#     [ # there's more than one output here, so you have to use square brackets to pass it in as an array.
#     Output('output-div','children'),Output('candlestick-graph','figure')
#     ],[Input('submit-button', 'n_clicks')]
#     ,[State('currency-pair', 'value')]
# )
# def update_candlestick_graph(n_clicks, value): # n_clicks doesn't get used, we only include it for the dependency.
#     # Now we're going to save the value of currency-input as a text file.
#     to_be_write = value
#     file_to_write = open("currency_pair.txt", "w")
#     file_to_write.write(to_be_write)
#     file_to_write.close()
#     # Wait until ibkr_app runs the query and saves the historical prices csv
#     while 'currency_pair_history.csv' not in listdir():
#         sleep(0.1)
#     # Read in the historical prices
#     df = pd.read_csv('currency_pair_history.csv')
#     # Remove the file 'currency_pair_history.csv'
#     remove("currency_pair_history.csv")
#     # Make the candlestick figure
#     fig = go.Figure(
#         data=[
#             go.Candlestick(
#                 x=df['date'],
#                 open=df['open'],
#                 high=df['high'],
#                 low=df['low'],
#                 close=df['close']
#             )
#         ]
#     )
#     # Give the candlestick figure a title
#     fig.update_layout(title=value)

    # # Return your updated text to currency-output, and the figure to candlestick-graph outputs
    # return ('Submitted query for ' + value), fig

# Callback for what to do when trade-button is pressed
@app.callback(
    [Output('candlestick-graph', 'figure'), Output('trade-output', 'children')],
    [Input('trade_submit', 'n_clicks')],
    [State('window', 'value'),
     State('backtest', 'value')],
    # We DON'T want to start executing trades just because n_clicks was initialized to 0!!!
    prevent_initial_call=True
)
def trade(n_clicks, window, backtest): # Still don't use n_clicks, but we need the dependency
    msg = 'the time window is ' + window + ' and the backtest length is ' + backtest
    # Make the message that we want to send back to trade-output
    trade_order = {
        "window": window,
        "backtest": backtest
    }
    js = json.dumps(trade_order)
    file = open('trade_order.txt', 'w')
    file.write(js)
    file.close()

    df = pd.read_csv('z_score.csv')
    df['date'] = pd.to_datetime(df['date'])
    date = df['date']
    zscore = df['zscore']
    buy = df['buy']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date, y=zscore,
                             mode='lines',
                             name='Z-score'))
    fig.add_trace(go.Scatter(x=date, y=buy,
                             mode='lines',
                             name='buy signal'))

    # Make our trade_order object -- a DICTIONARY.

    # Dump trade_order as a pickle object to a file connection opened with write-in-binary ("wb") permission:

    # Return the message, which goes to the trade-output div's "children" attribute.
    return fig, msg

# Run it!
if __name__ == '__main__':
    app.run_server(debug=True)

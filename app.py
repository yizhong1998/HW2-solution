# Fetches and displays a basic candlestick app.

import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from hw2_utils import *

#1)
cmt_rates = fetch_usdt_rates(2021)

def to_years(x):
    str_split = x.lower().split()
    if len(str_split) == 2:
        if str_split[1] == 'mo':
            return int(str_split[0]) / 12
        if str_split[1] == 'yr':
            return int(str_split[0])

#2) Create Figure
fig = go.Figure(
    data = [
        go.Surface(
            z = cmt_rates,
            y = cmt_rates.Date,
            x = [
                to_years(cmt_colname) for cmt_colname in list(
                    filter(lambda x:' ' in x, cmt_rates.columns.values)
                )
            ]
        )
    ]
)

#3) Figure layout
fig.update_layout(
    title = 'Bond Yields, 2021',
    scene = dict(
        xaxis_title = 'Maturity (years)',
        yaxis_title = 'Date',
        zaxis_title = 'APR (%)',
        zaxis = dict(ticksuffix = '%')
    ),
    autosize=False,
    width=1500,
    height=500,
    margin=dict(l=65, r=50, b=65, t=90)
)

# 4) Create a Dash app
app = dash.Dash(__name__)

# 5) Define a very simple layout -- just a plot inside a div. No inputs or outputs because the figure doesn't change.
app.layout = html.Div([dcc.Graph(id='3d-graph', figure=fig)])

# Run it!
if __name__ == '__main__':
    app.run_server(debug=True)

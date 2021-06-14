import datetime
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app

# Connect to your app pages
from apps import faturamento, pedidos


app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False,),
    dbc.Row([
        dbc.Col([
            dcc.Link('Faturado | ', href='/apps/faturamento'),
            dcc.Link('Pedidos | ', href='/apps/pedidos'),
        ], width=4),
    ]),
    html.Div(id='page-content', children=[])
], fluid=True)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/faturamento':
        return faturamento.layout
    if pathname == '/apps/pedidos':
        return pedidos.layout
    else:
        return faturamento.layout


if __name__ == '__main__':
    app.run_server(debug=True, port=3005)
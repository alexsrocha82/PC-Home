import datetime
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app

# Connect to pages
from apps import financeiro

# Connect to consltas
from datasets import consultas

# variaveis

app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([
            dcc.Link('Financeiro | ', href='/apps/financeiro')
        ], width=4),
        dbc.Col([html.P(id='time')], width=8),
    ]),
    dcc.Interval(id='update', n_intervals=0, interval=1*30000),
    html.Div(id='page-content', children=[])
], fluid=True)


@app.callback(Output('time', 'children'),
              [Input('update', 'n_intervals')])
def update_graph_scatter(n):
    t_now = datetime.datetime.now()
    t_atu = t_now.strftime('%d/%m/%Y %H:%M:%S')
    return [
        html.P(t_atu, style={'textAlign': 'right',
                              'color': '#FAFAFA',
                              'fontSize': 12,
                              'margin-top': '-10px'})
    ]


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/financeiro':
        return financeiro.layout
    else:
        return financeiro.layout


if __name__ == '__main__':
    app.run_server(debug=True, port=3003)
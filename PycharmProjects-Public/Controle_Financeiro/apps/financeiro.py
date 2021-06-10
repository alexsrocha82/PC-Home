from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import date

from app import app
from datasets import consultas

# tot receita
conn = consultas.conn
sql_tot_receita = consultas.tot_receita
tot_receita = pd.read_sql(sql_tot_receita, conn)
tot = tot_receita['valor'].sum()

# tot val categoria
categoria_val = consultas.categoria_val
tot_val_cat = pd.read_sql(categoria_val, conn)

# inicio container
layout = dbc.Container([
    # row 1
    dbc.Row([
        # row 1 column 1
        dbc.Col([
            html.H3('teste', style={'color': 'white', 'textAlign': 'center'}),
            html.P(tot, style={'color': 'white', 'textAlign': 'center'})
        ], className='create_container', width=3),
        # row 1 column 2
        dbc.Col([
            html.H3('teste', style={'color': 'white', 'textAlign': 'center'}),
            html.P(id='gastos')
        ], className='create_container', width=3),
        # row 1 column 3
        dbc.Col([
            html.H3('teste', style={'color': 'white', 'textAlign': 'center'}),
            html.P(id='gastos1')
        ], className='create_container', width=3),
        # row 1 column 4
        dbc.Col([
            dcc.Dropdown(id='categoria',
                         multi=False,
                         searchable=True,
                         value='Gts Geral',
                         placeholder= 'Selecione valor',
                         options=[{'label': c, 'value': c}
                                  for c in (tot_val_cat['categoria'].unique())]
                         ),
            html.P(id='gts')
        ], className='create_container', width=3),
    ]),
    # row 2
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='categoria1',
                         multi=False,
                         searchable=True,
                         value='Gts Geral',
                         placeholder= 'Selecione valor',
                         options=[{'label': c, 'value': c}
                                  for c in (tot_val_cat['categoria'].unique())]
                         ),
            html.P(id='gts1')
        ], className='create_container', width=3)
    ]),
    dcc.Interval(id='update', n_intervals=0, interval=1*120000)
], fluid=True)

# row 1 col 3 update teste ok
@app.callback(Output('gastos1', 'children'),
              [Input('update', 'n_intervals')])
def update_graph_scatter(n):
    tot_receita1 = pd.read_sql(sql_tot_receita, conn)  # assim funciona
    tot2 = tot_receita1['valor'].sum()
    return [
        html.P(tot2, style={'color': 'white', 'textAlign': 'center'})
    ]


# callback dropdown r1 c4
@app.callback(Output('gts', 'children'),
              Input('categoria', 'value'))
def update_confirmed(categoria):
    tot_cat = tot_val_cat[tot_val_cat['categoria'] == categoria]
    tot1 = tot_cat['total'].sum()
    return [
        html.P(tot1, style={'color': 'white', 'textAlign': 'center'})
    ]


# callback dropdown r1 c4
@app.callback(Output('gts1', 'children'),
              Input('categoria1', 'value'),
              #[Input('update', 'n_intervals')]
              )
def update_confirmed(categoria1):
    tot_val_cat1 = pd.read_sql(categoria_val, conn)
    tot_cat1 = tot_val_cat1[tot_val_cat1['categoria'] == categoria1]
    tot2 = tot_cat1['total'].sum()
    return [
        html.P(tot2, style={'color': 'white', 'textAlign': 'center'})
    ]


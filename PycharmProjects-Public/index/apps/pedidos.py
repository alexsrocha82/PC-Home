import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_core_components as dcc
import pandas as pd

from app import app
from datasets import consulta


# INICIO MAIN CONTAINER
layout = dbc.Container([
    # ROW 1
    dbc.Row([
        # ROW 1 COLUMN 1
        dbc.Col([
            html.H3('Pagina em Construção', style={'textAlign': 'center', 'color': '#FAFAFA'})
        ])
    ]),
], fluid=True)  # FIM MAIN CONTAINER

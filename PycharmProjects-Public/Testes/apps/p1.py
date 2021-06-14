import pathlib
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash_table as dt
import datetime
from datetime import date

# Connect to main app.py file
from app import app

# Connect to your app pages

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# dfv = pd.read_excel(DATA_PATH.joinpath("Fat_teste.xlsx"))

# INICIO MAIN CONTAINER
layout = dbc.Container([
    html.H1(id='tempo'),
    # row 1
    dbc.Row([
        # ROW 1 COLUMN 1
        dbc.Col(html.H3("Faturamento"), width=5),
        # row 1 column 2
        dbc.Col(dbc.Card('dfdfdf', color="primary", inverse=True)),
        # row 1 column 3
        dbc.Col(
            dbc.Card('dfddf', color="secondary", inverse=True)
        ),
        # row 1 column 4
        dbc.Col(dbc.Card('dfdfd', color="info", inverse=True)),
    ]),
    # row 2
    dbc.Row(
            [
                # row 2 column 1
                dbc.Col(dbc.Card(id='tot', color="success", inverse=True)),
                # row 2 column 2
                dbc.Col(dbc.Card(id='dfdfd', color="warning", inverse=True)),
                # row 2 column 3
                dbc.Col(dbc.Card('dfdfd', color="danger", inverse=True)),
            ],
            className="mb-4",
        ),
    # row 3 geral
    dbc.Row(id='col_test'),
    # update
    dcc.Interval(
        id='update',
        interval=1 * 15000,  # 30seg em milliseconds
        n_intervals=0
    )
], fluid=True)  # FIM MAIN CONTAINER


@app.callback(Output('tempo', 'children'),
              Input('update', 'n_intervals'))
def update_graph_live(update):
    return [
        html.H1('The time is: ' + str(datetime.datetime.now()))
    ]


@app.callback(Output('tot', 'children'),
              Input('update', 'n_intervals'))
def update_verde(update):
    df = pd.read_excel(r'F:\DOCUMENTOS\GIT\PC-Home\PycharmProjects-Public\Testes\datasets\Fat_teste.xlsx', sheet_name='Folha1',
                       engine='openpyxl')
    total = df['VAL_TOT'].sum()
    return [
        html.P(total)
    ]


@app.callback(Output('dfdfd', 'children'),
              Input('update', 'n_intervals'))
def update_amarelo(update):
    df = pd.read_excel(DATA_PATH.joinpath("Fat_teste.xlsx"))
    return [
        dbc.Row([
            dbc.Col([
                html.P(df['VAL_TOT'].sum(), style={'text-align': 'center'}),
            ]),
            dbc.Col([
                html.P(df['VAL_TOT'].max(), style={'text-align': 'center'}),
            ]),
        ]),
    ]


# column teste update
@app.callback(Output('col_test', 'children'),
              Input('update', 'n_intervals'))
def update_col_teste(update):
    teste = pd.read_excel(DATA_PATH.joinpath("Fat_teste.xlsx"))
    fat_uf = teste.groupby(['UF'])['VAL_TOT'].sum().reset_index()
    tab = teste[teste['UF'] == 'PR'][['NUM_PED', 'NOME_CLI', 'UF', 'VAL_TOT']].reset_index()
    colors = ['orange', '#d50000', '#7CB342', '#1565C0']
    return [
        dbc.Container([
            # row 3
            dbc.Row([
                # row 3 column 1
                dbc.Col([
                    dbc.Card(teste['VAL_TOT'].sum(), style={'text-align': 'center'}, color="primary", inverse=True),
                    html.Br(),
                    dbc.Card(teste['VAL_TOT'].sum(), style={'text-align': 'center'}, color="secondary", inverse=True),
                    html.Br(),
                    dbc.Card(teste['VAL_TOT'].sum(), style={'text-align': 'center'}, color="info", inverse=True),
                    html.Br(),
                    dbc.Card(teste['VAL_TOT'].sum(), style={'text-align': 'center'}, color="success", inverse=True),
                    html.Br(),
                    dbc.Card(teste['VAL_TOT'].sum(), style={'text-align': 'center'}, color="warning", inverse=True),
                ], width=3),
                # row 3 column 2
                dbc.Col([
                    html.Br(),
                    html.P(teste['VAL_TOT'].max(), style={'text-align': 'center', 'color': 'white'}),
                    html.Br(),
                    html.P(teste['VAL_TOT'].max(), style={'text-align': 'center', 'color': 'white'}),
                    html.Br(),
                    html.P(teste['VAL_TOT'].max(), style={'text-align': 'center', 'color': 'white'}),
                    html.Br(),
                ], className='card_container', width=3),
                # row 3 column 3
                dbc.Col([
                    dcc.Graph(config={'displayModeBar': 'hover'},
                              style={'height': '250px'},
                              figure={
                                  'data': [
                                      {'x': fat_uf['UF'], 'y': fat_uf['VAL_TOT'], 'type': 'bar'}
                                  ],
                                  'layout': {
                                      'title': 'Faturamento anual',
                                      'plot_bgcolor': '#1B2444',
                                      'paper_bgcolor': '#1B2444',
                                      'font': {'color': 'white'},
                                      'margin': dict(t=30, l=0, r=0, b=20),
                                  }
                              }
                              ),
                ], width=6),
            ]),
            # row 4
            html.Br(),
            dbc.Row([
                # row 4 column 1
                dbc.Col([
                    dcc.Graph(config={'displayModeBar': 'hover'},
                              style={'height': '250px'},
                              figure={
                                  'data': [go.Pie(
                                      labels=fat_uf['UF'],
                                      values=fat_uf['VAL_TOT'],
                                      marker=dict(colors=colors),
                                      hoverinfo='label+value+percent',
                                      textinfo='label+value',
                                      hole=.7

                                  )],
                                  'layout': go.Layout(
                                      title={'text': 'Total Cases: ',
                                             'y': .93, 'x': 0.5,
                                             'xanchor': 'center', 'yanchor': 'top'},
                                      titlefont={'color': 'white', 'size': 18},
                                      font=dict(family='sans-serif', color='white', size=12),
                                      hovermode='closest',
                                      paper_bgcolor='#1f2c56',
                                      plot_bgcolor='#1f2c56',
                                      legend={'orientation': 'h', 'bgcolor': '#1f2c56',
                                              'xanchor': 'center', 'x': 0.5, 'y': -0.7}
                                  )
                              }
                              ),
                ], width=6),
                # row 4 column 1
                dbc.Col([
                    dcc.Graph(config={'displayModeBar': 'hover'},
                              style={'height': '250px'},
                              figure={
                                  'data': [go.Pie(
                                      labels=fat_uf['UF'],
                                      values=fat_uf['VAL_TOT'],
                                      marker=dict(colors=colors),
                                      hoverinfo='label+value+percent',
                                      textinfo='label+value',
                                      hole=.7

                                  )],
                                  'layout': go.Layout(
                                      title={'text': 'Total Cases: ',
                                             'y': .93, 'x': 0.03,
                                             'xanchor': 'left', 'yanchor': 'top'},
                                      titlefont={'color': 'white', 'size': 18},
                                      font=dict(family='sans-serif', color='white', size=12),
                                      hovermode='closest',
                                      paper_bgcolor='#1f2c56',
                                      plot_bgcolor='#1f2c56',
                                  )
                              }
                              ),
                ], width=6)
            ]),
            html.Br(),
            # row 5
            dbc.Row([
                # row 5 column 1
                dbc.Col([
                    dt.DataTable(
                        columns=[
                            {'name': 'Pedido', 'id': 'NUM_PED', 'type': 'text'},
                            {'name': 'Cliente', 'id': 'NOME_CLI', 'type': 'text'},
                            {'name': 'UF', 'id': 'UF', 'type': 'text'},
                            {'name': 'Total', 'id': 'VAL_TOT', 'type': 'numeric'},
                        ],
                        virtualization=True,
                        style_cell={
                            'textAlign': 'left',
                            'min-width': '90px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                            'height': 'auto',
                            'whiteSpace': 'normal',
                            'padding': '5px'
                        },
                        style_header={
                            'fontWeight': 'bold',
                            'backgroundColor': '#E0E0E0',
                        },
                        style_as_list_view=False,
                        fixed_rows={'headers': True},
                        sort_action='native',
                        sort_mode='multi',
                        data=tab.to_dict('records'),
                        filter_action='native',
                        page_action="native",
                        page_current=0,
                        page_size=11
                    )
                ])
            ])
        ], fluid=True)
    ]

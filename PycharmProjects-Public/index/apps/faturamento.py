import pathlib
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from datetime import date

from app import app
from datasets import consulta

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_excel(DATA_PATH.joinpath("Fat_teste.xlsx"))
df['DT_EMISSAO2'] = pd.to_datetime(df['DT_EMISSAO'])
df['MES_NOME'] = df['DT_EMISSAO2'].dt.month_name()
df['MES'] = df['DT_EMISSAO2'].dt.month

# INICIO MAIN CONTAINER
layout = dbc.Container([
    # ROW 1
    dbc.Row([
        # ROW 1 COLUMN 1
        dbc.Col(html.H3("Faturamento"), width=5),
        # ROW 1 COLUMN 2
        dbc.Col([
            html.P('Ano', className='fix_label', style={'color': 'white'}),
            dcc.Slider(id='select_years',
                       included=False,
                       updatemode='drag',
                       tooltip={'always_visible': True},
                       min=2019,
                       max=2021,
                       step=1,
                       value=2021,
                       marks={str(yr): str(yr) for yr in range(2019,
                                                               2021 + 1)},
                       className='dcc_compon')
        ], width=7)
    ]),  # FIM ROW 1
    # ROW 2
    dbc.Row([
        # ROW 2 COLUMN 1
        dbc.Col([
            dbc.Col(id='fat_ano')
        ], className='create_container2 three columns'),
        # ROW 2 COLUMN 2
        dbc.Col([
            dbc.Col(id='fat_dia')
        ], className='create_container2 three columns'),
        # ROW 2 COLUMN 3
        dbc.Col([
            dbc.Col(children=[
                html.H6('Pedidos Dia', style={'textAlign': 'center', 'color': '#FAFAFA'}),
                html.P(id='ped_dia'),
            ])
        ], className='create_container2 three columns'),
        # ROW 2 COLUMN 4
        dbc.Col([
            dbc.Col(id='ped_pend')
        ], className='create_container2 three columns')
    ]),  # FIM ROW 2
    # ROW 3
    dbc.Row([
        # ROW 3 COLUMN 1
        dbc.Col([
            dcc.Graph(id='ft_line_chart', config={'displayModeBar': 'hover'}, style={'height': '250px'})
        ], className='create_container2 eight columns', style={'height': '260px'}),
        # ROW 3 COLUMN 2
        dbc.Col([
            html.Br(),
            dbc.Col(id='ft_res'),
            dbc.Col(id='ft_res1'),
            dbc.Col(id='ft_res2')
        ], className='create_container2', style={'height': '260px'}, width=2),
        # ROW 3 COLUMN 3
        dbc.Col([
            dbc.Col(id='bar_ft_uf3')
        ], className='create_container2', style={'height': '260px'}, width=2),
    ]),  # FIM ROW 3
    # ROW 4
    dbc.Row([
        # ROW 4 COLUMN 1
        dbc.Col([
            dcc.Graph(id='bar_ft_uf', config={'displayModeBar': 'hover'}, style={'height': '150px'})
        ], className='create_container2', style={'height': '160px'})
    ], className='row flex-display'),  # FIM ROW 4
    # TIME AUTO UPDATE - 5 Minuntos
    dcc.Interval(id='update', n_intervals=0, interval=1*300000),
    # TIME AUTO UPDATE - 10 Minutos
    dcc.Interval(id='update1', n_intervals=0, interval=1*600000),
], fluid=True)  # FIM MAIN CONTAINER


# CALLBACK  FAT ANO
@app.callback(Output('fat_ano', 'children'),
              [Input('update1', 'n_intervals')],
              [Input('select_years', 'value')])
def update_fat_ano(update1, select_years):
    #fat_ano = pd.read_sql(consulta.sql_fat_ano, consulta.conn)
    #current_year = fat_ano[fat_ano['ano'] == select_years]['faturado'].sum()
    current_year = df[df['ANO'] == 2019]['VAL_TOT'].sum()
    return [
        html.H6(children='Faturamento Ano',
                style={'textAlign': 'center',
                       'color': '#FAFAFA'}),

        html.P('R$ {0:,.2f}'.format(current_year),
               style={'textAlign': 'center',
                      'color': '#FAFAFA',
                      'fontSize': 15,
                      'margin-top': '-10px'})
    ]


# CALLBACK  FAT DIA
@app.callback(Output('fat_dia', 'children'),
              [Input('update', 'n_intervals')])
def update_fat_dia(update):
    # fat_d = pd.read_sql(consulta.sql_fat_dia, consulta.conn)
    # fat_dia = fat_d['faturado'].sum()
    fat_dia = df[df['DT_EMISSAO'] == df['DT_EMISSAO'].max()]['VAL_TOT'].sum()
    return [

        html.H6('Faturamento Dia', style={'textAlign': 'center', 'color': '#FAFAFA'}),
        html.P('R$ {0:,.2f}'.format(fat_dia),
               style={'textAlign': 'center',
                      'color': '#FAFAFA',
                      'fontSize': 15,
                      'margin-top': '-10px'}),
    ]


# CALLBACK PEDIDOS DIA
@app.callback(Output('ped_dia', 'children'),
              [Input('update', 'n_intervals')])
def update_graph_scatter(update):
    # pedi = pd.read_sql(consulta.sql_ped, consulta.conn)
    # val_ped_d = pedi['val1'].sum()
    val_ped_d = df[df['DT_EMISSAO'] == df['DT_EMISSAO'].max()]['VAL_TOT'].sum()
    return [
        html.P('R$ {0:,.2f}'.format(val_ped_d),
               style={'textAlign': 'center',
                      'color': '#FAFAFA',
                      'fontSize': 15,
                      'margin-top': '-10px'})
    ]


# CALLBACK  PEDIDO PENDENTE
@app.callback(Output('ped_pend', 'children'),
              [Input('update1', 'n_intervals')])
def update_ped_pend(update1):
    # ped_pend = pd.read_sql(consulta.sql_ped_pend, consulta.conn)
    # val_ped_pend = ped_pend['val_pend'].sum()
    # qtd_ped_pend = ped_pend['c5_num'].count()
    val_ped_pend = 124.50
    qtd_ped_pend = 5
    return [
        html.H6('Val Ped Pendente : R$ 50201,22', # + 'R$ {0:,.2f}'.format(val_ped_pend),
                style={'textAlign': 'left', 'color': '#FAFAFA', 'fontSize': 15}),
        html.H6('Qtd Ped Pendente : 5',    # + qtd_ped_pend.astype(str),
                style={'textAlign': 'left', 'color': '#FAFAFA', 'fontSize': 15}),
    ]


# CALLBACK LINE FAT_MES
@app.callback(Output('ft_line_chart', 'figure'),
              [Input('select_years', 'value')],
              [Input('update1', 'n_intervals')])
def update_line_mes(select_years, update1):
    # sql_fat1 = pd.read_sql(consulta.sql_fat1, consulta.conn)
    # sql_fat1['d2_emissao'] = pd.to_datetime(sql_fat1['d2_emissao'])
    # sql_fat1['mes_nome'] = sql_fat1['d2_emissao'].dt.month_name()
    # fat_mes = sql_fat1.groupby(['ano', 'mes', 'mes_nome'])['faturado'].sum().reset_index()
    # fat_mes1 = fat_mes[(fat_mes['ano'].astype(int) == select_years)].sort_values(by=['ano', 'mes'], ascending=True)
    fat_mes = df.groupby(['ANO', 'MES', 'MES_NOME'])['VAL_TOT'].sum().reset_index()
    fat_mes1 = fat_mes[(fat_mes['ANO'].astype(int) == 2019)].sort_values(by=['ANO', 'MES'], ascending=True)

    return {
        'data': [go.Scatter(
            x=fat_mes1['MES_NOME'],
            y=fat_mes1['VAL_TOT'],
            text=fat_mes1['VAL_TOT'],
            texttemplate='R$ ' + '%{text:,.0f}',
            textposition='bottom center',
            mode='markers+lines+text',
            line=dict(width=2, color='#03A9F4'),
            marker=dict(color='#03A9F4', size=8, symbol='circle', line=dict(color='#03A9F4', width=2)),
            hoverinfo='text',
            # hovertext=
            # '<b>Mes</b>: ' + fat_mes1['MES_NOME'].astype(str) + '<br>' +
            # '<b>Sales</b>: R$ ' + [f'{x:,.0f}' for x in fat_mes1['VAL_TOT']] + '<br>'
        )],

        'layout': go.Layout(
            title={'text': 'Faturado por Mês ano 2019',
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 15},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1B2444',
            plot_bgcolor='#1B2444',
            legend={'orientation': 'h',
                    'bgcolor': 'white',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t=30, l=0, r=0, b=20),
            xaxis=dict(title='<b></b>',
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(
                color='white',
                showline=False,
                showgrid=False,
                showticklabels=False,
                linecolor='white',
                linewidth=1,
                ticks='outside',
                tickfont=dict(
                    family='Aerial',
                    color='white',
                    size=12
                ))
        )
    }


# CALLBACK RESUMO FATURADO
@app.callback(Output('ft_res', 'children'),
              [Input('select_years', 'value')],
              [Input('update1', 'n_intervals')])
def update_faturado(select_years, update1):
    # res_fat_ano = pd.read_sql(consulta.sql_fat_ano, consulta.conn)
    # current_year = res_fat_ano[res_fat_ano['ano'] == select_years]['faturado'].sum()
    current_year = df[df['ANO'] == 2019]['VAL_TOT'].sum()

    return [
        html.H6(children='Ano Atual',
                style={'textAlign': 'center',
                       'color': '#FAFAFA'}),

        html.P('R$ {0:,.2f}'.format(current_year),
               style={'textAlign': 'center',
                      'color': '#FAFAFA',
                      'fontSize': 15,
                      'margin-top': '-10px'})
    ]


# CALLBACK RESUMO FAT PREV
@app.callback(Output('ft_res1', 'children'),
              [Input('select_years', 'value')],
              [Input('update1', 'n_intervals')])
def update_fat_prev(select_years, update1):
    # res_fat_ano = pd.read_sql(consulta.sql_fat_ano, consulta.conn)
    # fat_ano_prev = res_fat_ano.groupby(['ano'])['faturado'].sum().reset_index()
    # fat_ano_prev['py'] = fat_ano_prev['faturado'].shift(1)
    # prev_year = fat_ano_prev[fat_ano_prev['ano'] == select_years]['py'].sum()
    prev_year = df[df['ANO'] == 2019]['VAL_TOT'].sum()

    return [
        html.H6(children='Ano Anterior',
                style={'textAlign': 'center',
                       'color': '#FAFAFA'}),

        html.P('R$ {0:,.2f}'.format(prev_year),
               style={'textAlign': 'center',
                      'color': '#FAFAFA',
                      'fontSize': 15,
                      'margin-top': '-10px'})
    ]


# CALLBACK RESUMO VAR FAT
@app.callback(Output('ft_res2', 'children'),
              [Input('select_years', 'value')],
              [Input('update1', 'n_intervals')])
def update_var_fat(select_years, update1):
    # res_fat_ano = pd.read_sql(consulta.sql_fat_ano, consulta.conn)
    # fat_ano_grow = res_fat_ano.groupby(['ano'])['faturado'].sum().reset_index()
    # fat_ano_grow['growth'] = fat_ano_grow['faturado'].pct_change()
    # fat_ano_grow['growth'] = fat_ano_grow['growth'] * 100
    # fat_ano_grow1 = fat_ano_grow[fat_ano_grow['ano'] == select_years]['growth'].sum()
    fat_ano_grow1 = 20

    return [
        html.H6(children='Variação Fat.',
                style={'textAlign': 'center',
                       'color': '#FAFAFA'}),

        html.P('{0:,.2f} %'.format(fat_ano_grow1),
               style={'textAlign': 'center',
                      'color': '#FAFAFA',
                      'fontSize': 15,
                      'margin-top': '-10px'})
    ]


# CALLBACK FAT ANUAL BARRA
@app.callback(Output('bar_ft_uf3', 'children'),
              [Input('update1', 'n_intervals')])
def update_bar_fat(update1):
    # fat_ano = pd.read_sql(consulta.sql_fat_ano, consulta.conn)
    fat_ano = df[df['ANO'] == 2019]['VAL_TOT'].sum()
    return [
        dcc.Graph(config={'displayModeBar': 'hover'},
                  style={'height': '250px'},
                  figure={
                      'data': [
                          {'x': fat_ano['ANO'], 'y': fat_ano['VAL_TOT'], 'type': 'bar'}
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
    ]


# CALLBACK GRAFICO BARRA FAT_UF
@app.callback(Output('bar_ft_uf', 'figure'),
              [Input('select_years', 'value')],
              [Input('update1', 'n_intervals')])
def update_graph_uf(select_years, update1):
    # fat_u = pd.read_sql(consulta.sql_fat_uf, consulta.conn)
    # fat_uf = fat_u.groupby(['ano', 'uf'])['faturado'].sum().reset_index()
    # fat_uf1 = fat_uf[(fat_uf['ano'] == select_years)].sort_values(by=['faturado'], ascending=False)
    fat_uf = df.groupby(['ANO', 'UF'])['VAL_TOT'].sum().reset_index()
    fat_uf1 = fat_uf[(fat_uf['ANO'] == 2019)].sort_values(by=['VAL_TOT'], ascending=False)
    return {
        'data': [go.Bar(
            y=fat_uf1['VAL_TOT'],
            x=fat_uf1['UF'],
            text=fat_uf1['VAL_TOT'],
            textposition='auto',
            texttemplate=(fat_uf1['VAL_TOT'].astype(float)/1000000).round(2).astype(str) + "MM",
            orientation='v',
            marker=dict(color='white'),
            hoverinfo='text',
            # hovertext=
            # '<b>Ano</b>: ' + fat_uf1['ANO'].astype(str) + '<br>' +
            # '<b>Sales</b>: R$ ' + [f'{x:,.0f}' for x in fat_uf1['VAL_TOT']] + '<br>'
        )],

        'layout': go.Layout(
            title={'text': 'Vendas por Estado ano 2019',
                   'y': 0.99,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 12},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1B2444',
            plot_bgcolor='#1B2444',
            legend={'orientation': 'v',
                    'bgcolor': 'white',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(t=30, b=30, r=0, l=0),
            xaxis=dict(title='<b></b>',
                       color='white',
                       showline=False,
                       showgrid=False,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
            yaxis=dict(title='<b></b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       ))
        )
    }

import datetime
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Connect to main app.py file
from app import app

# Connect to your app pages
from apps import p1, p2


app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False,),
    dbc.Row([
        dbc.Col([
            dcc.Link('Pag 1 | ', href='/apps/p1'),
            dcc.Link('Pag 2 | ', href='/apps/p2'),
        ], width=4),
    ]),
    html.Div(id='page-content', children=[])
], fluid=True)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/p1':
        return p1.layout
    if pathname == '/apps/p2':
        return p2.layout
    else:
        return p1.layout


if __name__ == '__main__':
    app.run_server(debug=True, port=3001)

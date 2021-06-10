import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd



url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

# unfpivot dataframe
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], value_vars=date1, var_name='date', value_name='confirmed')
date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'],value_vars = date2, var_name = 'date', value_name = 'deaths')
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'],value_vars = date3, var_name = 'date', value_name = 'recovered')

# mferging dataframe
covid_data = total_confirmed.merge(right = total_deaths, how = 'left', on = ['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])
covid_data = covid_data.merge(right = total_recovered, how = 'left', on = ['Province/State', 'Country/Region', 'date', 'Lat', 'Long'])

# converting data columns from strig to date
covid_data['date'] = pd.to_datetime(covid_data['date'])

# check missing values
covid_data.isna().sum()

#replace naN with 0
covid_data['recovered'] = covid_data['recovered'].fillna(0)

# create neu column
# traz last update
covid_data['active'] = covid_data['confirmed'] - covid_data['deaths'] - covid_data['recovered']
# soma casos confirmados
covid_cases = covid_data.groupby(['date'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()

# soma casos novos
new_covid_confirmed = covid_cases['confirmed'].iloc[-1] - covid_cases['confirmed'].iloc[-2]
# percentual novos casos
perc_covid_confirmed = round(((covid_cases['confirmed'].iloc[-1] - covid_cases['confirmed'].iloc[-2]) / covid_cases['confirmed'].iloc[-1]) * 100, 2)

# soma deaths novos
new_covid_death = covid_cases['deaths'].iloc[-1] - covid_cases['deaths'].iloc[-2]
# percentual novos deaths
perc_covid_death = round(((covid_cases['deaths'].iloc[-1] - covid_cases['deaths'].iloc[-2]) / covid_cases['deaths'].iloc[-1]) * 100, 2)

# soma recovered novos
new_covid_recovered = covid_cases['recovered'].iloc[-1] - covid_cases['recovered'].iloc[-2]
# percentual novos recovered
perc_covid_recovered = round(((covid_cases['recovered'].iloc[-1] - covid_cases['recovered'].iloc[-2]) / covid_cases['recovered'].iloc[-1]) * 100, 2)

# soma active novos
new_covid_active = covid_cases['active'].iloc[-1] - covid_cases['active'].iloc[-2]
# percentual novos active
perc_covid_active = round(((covid_cases['active'].iloc[-1] - covid_cases['active'].iloc[-2]) / covid_cases['active'].iloc[-1]) * 100, 2)

# create dictionary os list
covid_data_list = covid_data[['Country/Region','Lat','Long']]
dict_of_locations = covid_data_list.set_index('Country/Region')[['Lat','Long']].T.to_dict('dict')

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([
    # CONTAINER ROW 1
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('corona-logo.jpg'),
                     id= 'corona-image',
                     style= {
                         'height': '60px',
                         'width': 'auto',
                         'margin-bottom': '25px'
                     })
        ], className= 'one-third column'),   # row 1 , column 1

        html.Div([
            html.Div([
                html.H3('Covid - 19', style={'margin-bottom': '0px', 'color': 'white'}),
                html.H5('Track Covid - 19 Cases', style={'margin-bottom': '0px', 'color': 'white'})
            ])
        ], className= 'one-half column', id= 'title'),   # row 1 , column 2
        html.Div([
            html.H6('Last Update: ' + str(covid_data['date'].iloc[-1].strftime('%B %d, %Y')) + ' 00:01 (UTC)',
                    style={'color': 'orange'})
        ], className= 'one-third column', id= 'title1')  # row 1 , column 3
    ], id= 'header', className= 'row flex-display', style={'margin-bottom': '25px'}),  #fim container row 1
    # CONTAINER ROW 2
    html.Div([
        html.Div([
            # titulo
            html.H6(children= 'Global Cases',
                    style= {'textAlign': 'center',
                            'color': 'white'}),
            # paragrafo 1 - valor casos
            html.P(f"{covid_cases['confirmed'].iloc[-1]:,.0f}",
                    style={'textAlign': 'center',
                           'color': 'orange',
                           'fontSize': 30}),
            # paragrafo 2 - valor novos casos
            html.P('Novos: ' + f"{new_covid_confirmed:,.0f}" + ' (' +
                   str(perc_covid_confirmed)+ ' %)',
                   style={'textAlign': 'center',
                          'color': 'orange',
                          'fontSize': 13,
                          'margin-top': '-18px'})
        ], className= 'card_container three columns'),  # row 2 , column 1
        html.Div([
            # titulo
            html.H6(children='Global Deaths',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            # paragrafo 1 - valor casos deaths
            html.P(f"{covid_cases['deaths'].iloc[-1]:,.0f}",
                   style={'textAlign': 'center',
                          'color': '#d50000',
                          'fontSize': 30}),
            # paragrafo 2 - valor novos deaths
            html.P('Novos: ' + f"{new_covid_death:,.0f}" + ' (' +
                   str(perc_covid_death) + ' %)',
                   style={'textAlign': 'center',
                          'color': '#d50000',
                          'fontSize': 13,
                          'margin-top': '-18px'})
        ], className='card_container three columns'),  # row 2 , column 2
html.Div([
            # titulo
            html.H6(children='Global Recovered',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            # paragrafo 1 - valor casos recovered
            html.P(f"{covid_cases['recovered'].iloc[-1]:,.0f}",
                   style={'textAlign': 'center',
                          'color': '#7CB342',
                          'fontSize': 30}),
            # paragrafo 2 - valor novos casos recovered
            html.P('Novos: ' + f"{new_covid_recovered:,.0f}" + ' (' +
                   str(perc_covid_recovered) + ' %)',
                   style={'textAlign': 'center',
                          'color': '#7CB342',
                          'fontSize': 13,
                          'margin-top': '-18px'})
        ], className='card_container three columns'),  # row 2 , column 3
html.Div([
            # titulo
            html.H6(children='Global Active',
                    style={'textAlign': 'center',
                           'color': 'white'}),
            # paragrafo 1 - valor casos active
            html.P(f"{covid_cases['active'].iloc[-1]:,.0f}",
                   style={'textAlign': 'center',
                          'color': '#1565C0',
                          'fontSize': 30}),
            # paragrafo 2 - valor novos casos active
            html.P('Novos: ' + f"{new_covid_active:,.0f}" + ' (' +
                   str(perc_covid_active) + ' %)',
                   style={'textAlign': 'center',
                          'color': '#1565C0',
                          'fontSize': 13,
                          'margin-top': '-18px'})
        ], className='card_container three columns'),  # row 2 , column 4
    ], className= 'row flex display'),   # fim container row 2
    # CONTAINER ROW 3
    html.Div([
        # row 3 column 1
        html.Div([
            html.P('Select Country: ', className= 'fix_label', style= {'color': 'white'}),
            dcc.Dropdown(id= 'w_countries',
                         multi= False,
                         searchable= True,
                         value= 'Brazil',
                         placeholder= 'Select Countries',
                         options= [{'label': c, 'value': c}
                                   for c in (covid_data['Country/Region'].unique())],className= 'dcc_compon'),
            html.P('New Cases' + ' ' + str(covid_data['date'].iloc[-1].strftime('%B %d, %Y')),
                   className= 'fix_label', style={'text-align': 'center', 'color': 'white', 'fontSize': 13}),
            dcc.Graph(id= 'confirmed', config={'displayModeBar': False}, className= 'dcc_compon',
                      style={'margin-top': '20px'}),
            dcc.Graph(id= 'deaths', config={'displayModeBar': False}, className= 'dcc_compon',
                      style={'margin-top': '20px'}),
            dcc.Graph(id= 'recovered', config={'displayModeBar': False}, className= 'dcc_compon',
                      style={'margin-top': '20px'}),
            dcc.Graph(id='active', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
        ], className= 'create_container three columns'),
        # row 3 column 2
        html.Div([
            dcc.Graph(id= 'pie_chart', config= {'displayModeBar': 'hover'}),
        ], className= 'create_container four columns'),
        # row 3 column 3
        html.Div([
            dcc.Graph(id='line_chart', config={'displayModeBar': 'hover'}),
        ], className='create_container five columns'),
    ], className= 'row flex-display'),    # fim container row 3
    # CONTAINER ROW 4
    html.Div([
        # row 4 column 1
        html.Div([
            dcc.Graph(id='map_chart', config={'displayModeBar': 'hover'}),
        ], className='create_container1 twelve columns'),
    ], className='row flex-display')
], id= 'mainContainer', style={'display': 'flex', 'flex-direction': 'column'})  # Container geral / main

# callback confirmed
@app.callback(Output('confirmed','figure'),
              Input('w_countries','value'))
def update_confirmed(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    value_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1] - \
                      covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2]
    delta_confirmed = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-2] - \
                      covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-3]

    return {
        'data': [go.Indicator(
            mode='number+delta',
            value=value_confirmed,
            delta= {'reference': delta_confirmed,
                    'position': 'right',
                    'valueformat': ',g',
                    'relative': False,
                    'font': {'size': 12}},
            number= {'valueformat': ',',
                     'font': {'size': 15}},
            domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'New Confirmed',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color= 'orange'),
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            height= 50,
        )
    }

# callback deaths
@app.callback(Output('deaths','figure'),
              Input('w_countries','value'))
def update_deaths(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    value_deaths = covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-1] - \
                   covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-2]
    delta_deaths = covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-2] - \
                   covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-3]

    return {
        'data': [go.Indicator(
            mode='number+delta',
            value=value_deaths,
            delta= {'reference': delta_deaths,
                    'position': 'right',
                    'valueformat': ',g',
                    'relative': False,
                    'font': {'size': 12}},
            number= {'valueformat': ',',
                     'font': {'size': 15}},
            domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'New Deaths',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color= '#d50000'),
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            height= 50,
        )
    }

# callback recovered
@app.callback(Output('recovered','figure'),
              Input('w_countries','value'))
def update_recovered(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    value_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1] - \
                      covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2]
    delta_recovered = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-2] - \
                      covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-3]

    return {
        'data': [go.Indicator(
            mode='number+delta',
            value=value_recovered,
            delta= {'reference': delta_recovered,
                    'position': 'right',
                    'valueformat': ',g',
                    'relative': False,
                    'font': {'size': 12}},
            number= {'valueformat': ',',
                     'font': {'size': 15}},
            domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'New Recovered',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color= '#7CB342'),
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            height= 50,
        )
    }

# callback active
@app.callback(Output('active','figure'),
              Input('w_countries','value'))
def update_active(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    value_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1] - \
                   covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2]
    delta_active = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-2] - \
                   covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-3]

    return {
        'data': [go.Indicator(
            mode='number+delta',
            value=value_active,
            delta= {'reference': delta_active,
                    'position': 'right',
                    'valueformat': ',g',
                    'relative': False,
                    'font': {'size': 12}},
            number= {'valueformat': ',',
                     'font': {'size': 15}},
            domain={'y': [0, 1], 'x': [0, 1]}
        )],
        'layout': go.Layout(
            title={'text': 'New Active',
                   'y': 1,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            font=dict(color= '#1565C0'),
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            height= 50,
        )
    }

# callback pie_chart
@app.callback(Output('pie_chart','figure'),
              Input('w_countries','value'))
def update_pie_chart(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    confirmed_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['confirmed'].iloc[-1]
    deaths_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['deaths'].iloc[-1]
    recovered_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['recovered'].iloc[-1]
    active_value = covid_data_2[covid_data_2['Country/Region'] == w_countries]['active'].iloc[-1]
    colors = ['orange', '#d50000', '#7CB342', '#1565C0']

    # PIE CHART
    return {
        'data': [go.Pie(
            labels=['Confirmed', 'Deaths', 'Recovered', 'Active'],
            values=[confirmed_value, deaths_value, recovered_value, active_value],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7

        )],
        'layout': go.Layout(
            title={'text': 'Total Cases: ' + (w_countries),
                   'y': .93, 'x': 0.5,
                   'xanchor': 'center', 'yanchor': 'top'},
            titlefont={'color': 'white', 'size': 18},
            font=dict(family='sans-serif', color='white', size= 12),
            hovermode= 'closest',
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            legend={'orientation': 'h', 'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7}
        )
    }

# callback line_chart
@app.callback(Output('line_chart','figure'),
              Input('w_countries','value'))
def update_line_chart(w_countries):
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region'] == w_countries][
        ['Country/Region', 'date', 'confirmed']].reset_index()
    covid_data_3['daily confirmed'] = covid_data_3['confirmed'] - covid_data_3['confirmed'].shift(1)
    covid_data_3['Rolling Ave.'] = covid_data_3['daily confirmed'].rolling(window=7).mean()
    # LINE CHART
    return {
        'data': [go.Bar(
            x=covid_data_3['date'].tail(30),
            y=covid_data_3['daily confirmed'].tail(30),
            name='Daily Confirmed Cases',
            marker=dict(color='orange'),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['daily confirmed'].tail(30)] + '<br>' +
            '<b>Country</b>: ' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>'
        ),
            go.Scatter(
                x=covid_data_3['date'].tail(30),
                y=covid_data_3['Rolling Ave.'].tail(30),
                mode='lines',
                name='Rolling Average last 7 days',
                line=dict(width=3, color='#FF00FF'),
                hoverinfo='text',
                hovertext=
                '<b>Date</b>: ' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
                '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_3['Rolling Ave.'].tail(30)] + '<br>'
            )
        ],
        'layout': go.Layout(
            title={'text': 'Daily Confirmed Cases: ' + (w_countries),
                   'y': .93, 'x': 0.5,
                   'xanchor': 'center', 'yanchor': 'top'},
            titlefont={'color': 'white', 'size': 18},
            font=dict(family='sans-serif', color='white', size= 12),
            hovermode= 'closest',
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            legend={'orientation': 'h', 'bgcolor': '#1f2c56',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Daily Confirmed Cases</b>',color='white',showline=True,showgrid=True,
                       showticklabels=True,linecolor='white',linewidth=1,ticks='outside',
                       tickfont=dict(family='Arial',color='white',size=12)),
            yaxis=dict(title='<b>Daily Confirmed Cases</b>', color='white', showline=True, showgrid=True,
                       showticklabels=True, linecolor='white', linewidth=1, ticks='outside',
                       tickfont=dict(family='Arial', color='white', size=12)
                       ),
        )
    }

# callback map_chart
@app.callback(Output('map_chart','figure'),
              Input('w_countries','value'))
def update_map_chart(w_countries):
    covid_data_4 = covid_data.groupby(['Lat', 'Long', 'Country/Region'])[
        ['confirmed', 'deaths', 'recovered', 'active']].max().reset_index()
    covid_data_5 = covid_data_4[covid_data_4['Country/Region'] == w_countries]

    if w_countries:
        zoom=2
        zoom_lat= dict_of_locations[w_countries]['Lat']
        zoom_long= dict_of_locations[w_countries]['Long']

    # MAP CHART
    return {
        'data': [go.Scattermapbox(
            lon=covid_data_5['Long'],
            lat=covid_data_5['Lat'],
            mode='markers',
            marker=go.scattermapbox.Marker(size=covid_data_5['confirmed'] / 1500,
                                           color=covid_data_5['confirmed'],
                                           colorscale='HSV',
                                           showscale=False,
                                           sizemode='area',
                                           opacity=0.3),
            hoverinfo='text',
            hovertext=
            '<b>Country</b>: ' + covid_data_5['Country/Region'].astype(str) + '<br>' +
            '<b>Longitude</b>: ' + covid_data_5['Long'].astype(str) + '<br>' +
            '<b>Latitude</b>: ' + covid_data_5['Lat'].astype(str) + '<br>' +
            '<b>Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['confirmed'].tail(30)] + '<br>' +
            '<b>Death Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['deaths'].tail(30)] + '<br>' +
            '<b>Recovered Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['recovered'].tail(30)] + '<br>' +
            '<b>Active Cases</b>: ' + [f'{x:,.0f}' for x in covid_data_5['active'].tail(30)] + '<br>'
        )],
        'layout': go.Layout(
            hovermode= 'x',
            paper_bgcolor= '#1f2c56',
            plot_bgcolor= '#1f2c56',
            margin=dict(r=0, l=0, b=0, t=0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoiYWxleHNyb2NoYSIsImEiOiJja2xsOHM0NmcwOXdoMnVsY3BuaXMxZzJlIn0.XS1c3S8CkXaxyETEMmiH0Q',
                center= go.layout.mapbox.Center(lat=zoom_lat, lon=zoom_long),
                style='dark',
                zoom=zoom,
            ),
            autosize=True
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
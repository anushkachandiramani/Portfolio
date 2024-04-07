"""
HW3 code
Alyssa, Anushka, Bryce
File: sunspot.py
Description: Makes the Sunspot Dashboard with data from sunspot.db
accessed through api in sunspot_api.py
"""

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from datetime import datetime as dt
from sunspot_api import SunspotAPI
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

# load styling template
load_figure_template('CYBORG')

def main():
    # initialize the app object
    api = SunspotAPI()
    api.connect("sunspot.db")

    # create the dash app
    app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

    # image urls
    image_urls = {
        'SOHO EIT 171': "https://soho.nascom.nasa.gov/data/realtime/eit_171/1024/latest.jpg",
        'SOHO EIT 195': "https://soho.nascom.nasa.gov/data/realtime/eit_195/512/latest.jpg",
        'SOHO EIT 284': "https://soho.nascom.nasa.gov/data/realtime/eit_284/512/latest.jpg",
        'SOHO EIT 304': "https://soho.nascom.nasa.gov/data/realtime/eit_304/512/latest.jpg",
        'SOHO HMI Intensitygram': "https://soho.nascom.nasa.gov/data/realtime/hmi_igr/1024/latest.jpg",
        'SOHO HMI Magnetogram': "https://soho.nascom.nasa.gov/data/realtime/hmi_mag/1024/latest.jpg",
        'SDO/HMI Continuum': "https://soho.nascom.nasa.gov/data/realtime/hmi_igr/512/latest.jpg",
        'SOHO LASCO C2': "https://soho.nascom.nasa.gov/data/realtime/c2/512/latest.jpg",
        'SOHO LASCO C3': "https://soho.nascom.nasa.gov/data/realtime/c3/512/latest.jpg"
    }

    # create list of integers representing decaves from 1810 to 2000.
    decades = list(range(1810, 2001, 10))  
    decades = [{'label': f'{decade}s', 'value': decade} for decade in range(1820, 2020, 10)]

    # create dictionary with label - value pairs
    dropdown_options = [{'label': key, 'value': value} for key, value in image_urls.items()]

    # create the layout
    app.layout = html.Div([
        # title
        html.H1('Sunspot Data Visualization',
                style={'textAlign': 'center'}),

        # year range slider
        html.Label('Select Year Range:'),
        dcc.RangeSlider(
            id='year_range',
            min=1800, max=2000, 
            value=[1800, 2000],
            marks={str(year): str(year) for year in range(1800, 2001, 20)},
            step=1),
        
        # top left block
        html.Div([
            # smoothing period slider
            html.Label('Select Smoothing Period (months):'),
            dcc.Slider(
                id='smoothing_period',
                min=1, # 1 - 24 months
                max=24,
                value=12, # default is 12 months
                marks={str(month): str(month) for month in range(1, 25)},
                step=1),
            # sunspot graph
            dcc.Graph(
                id='sunspot-graph')
            ],
            style={
                'display': 'inline-block',
                'width': '49%'
            }
        ),

        # top right block
        html.Div([
            # sunspot cycle period slider
            html.Label('Select Sunspot Cycle Period (years):'),
            dcc.Slider(
                id='cycle_period',
                min=9,
                max=15,
                value=11.0,
                marks={i: {'label': str(i)} for i in range(9, 16)},
                step=0.1),
            # sunspot cycler period graph
            dcc.Graph(id='cycle-graph')
            ],
            style={
                'display': 'inline-block',
                'width': '49%'
            }
        ),

        # bottom left block
        html.Div([
            # select image drop down, show image
            html.Label('Select Live-Updated Image:'),
            dcc.Dropdown(
                id='image-dropdown',
                options=dropdown_options,
                value=list(image_urls.values())[0]),
            # add image
            html.Img(
                id='sun-image',
                style={
                    'display': 'inline-block',
                    'width': '75%'
                }
            )],
            style={
                'display': 'inline-block',
                'width': '49%'
            }
        ),

        # bottom right block
        html.Div([
            # select decade dropdown
            html.Label('Select Decade:'),
            dcc.Dropdown(
                id='decade-dropdown',
                options=decades,
                value=1820,  # default value
            ),
            # add histogram
            dcc.Graph(id='sunspot-histogram'),
        ], style={
            'display': 'inline-block',
            'width': '49%',
            'vertical-align': 'top'
        }),

    ])

    # define first callback
    @app.callback(
        Output('sunspot-graph', 'figure'),
        Input('year_range', 'value'),
        Input('smoothing_period', 'value')
    )

    # sunspot activity over time graph
    def update_line_graph(year_range, smoothing_period):
        """
        Function: update_graph - updates Sunspot Activity over Time graph and layout
        
        Parameters:
            year_range: tuple containing start and end year obtained from dash slider
            smoothing_period: range of time to smooth over obtained from dash slider
        
        Returns: graphed figure
        """
        # extract tuple from callback input
        start_year, end_year = year_range

        # get start and end date from api
        df = api.get_sunspot_amt_range(start_year, end_year)

        # smooth dataframe based on window from callback input
        df['Smoothed'] = df['Daily_Sunspot_Total'].rolling(window=smoothing_period).mean()

        # plot figure
        fig = px.line(
            df,
            x='Date_Fraction',
            y='Daily_Sunspot_Total',
            template="plotly_dark"
        )

        # add title
        fig.update_layout(title_text='Sunspot Activity over Time', title_x=0.5)

        # add labels to x and y axis
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Sunspot Activity")

        fig.add_scatter(
            x=df['Date_Fraction'],
            y=df['Smoothed'],
            mode='lines',
            name='Smoothed'
        )
        fig.update_traces(
            overwrite=True,
            selector=dict(name='Smoothed'),
            line=dict(color='red', width=4)
        )

        return fig


    # Second callback
    @app.callback(
        Output('cycle-graph', 'figure'),
        Input('year_range', 'value'),
        Input('cycle_period', 'value')
    )

    # second graph - sunspot cycle variability
    def update_cycle_graph(year_range, cycle_period):
        """
        Function: update_cycle_graph - updates Sunspot Cycle Variability graph and layout
        
        Paramers:
            year_range: tuple containing start and end year obtained from dash slider
            cycle_period: period over which to cycle obtained from dash slider

        Returns:  graphed figure
        """
        # extract tuple from callback input
        start_year, end_year = year_range

        # gets data for data range
        df = SunspotAPI.get_sunspot_amt_range(start_year, end_year)

        # take only the cycler period from callback input
        df['Cycle_Year'] = df['Date_Fraction'] % cycle_period

        # plot figure
        fig = px.scatter(
            df,
            x='Cycle_Year',
            y='Daily_Sunspot_Total',
            title='Sunspot Cycle Variability',
            labels={
                'Cycle_Year': 'Years',
                'Daily_Sunspot_Total': '# of Sunspots'
            },
            template="plotly_dark"
        )

        # add title
        fig.update_layout(title_text='Sunspot Cycle Variability', title_x=0.5)

        return fig

    # third callback for image
    @app.callback(
        Output('sun-image', 'src'),
        Input('image-dropdown', 'value')
    )

    # runs url
    def update_image_src(selected_url):
        """
        Function: update_image_src - updates source url for a live-updated image from url
        
        Parameters:
            selected_url: string representing url to obtain image from
            
        Returns: the source url
        """
        return selected_url


    # fourth callback
    @app.callback(
        Output('sunspot-histogram', 'figure'),
        Input('decade-dropdown', 'value')
    )

    # third graph, daily sunpot total count histogram
    def update_histogram(selected_decade):
        """
        Function: update histogram - updates Count of Daily Sunspot Totals over Chosen Decade
            graph and layout
        
        Parameters:
            selected_decade: integer representing start year of decade 
                obtained from dash dropdown menu
            
        Returns: graphed figure
        """
        # establish start and end years
        start_year = selected_decade
        end_year = start_year + 9

        # get selected data
        df = SunspotAPI.get_sunspot_amt_range(start_year, end_year)

        # generate histogram
        fig = px.histogram(
            df, 
            x='Daily_Sunspot_Total', 
            title=f'Sunspot Distribution: {start_year}s', 
            template = 'plotly_dark'
        )

        # add title
        fig.update_layout(
            title_text='Count of Daily Sunspot Totals over Chosen Decade', 
            title_x=0.5
        )

        # add labels to x and y axis
        fig.update_xaxes(title_text="Daily Sunspot Total")
        fig.update_yaxes(title_text="Count over Decade")
        
        return fig

    # run server
    app.run_server(debug=True)

if __name__ == '__main__':
    main()



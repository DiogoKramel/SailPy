import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_daq as daq
import dash_table
import pandas as pd

from callbacks import resultsappendagesplots
from app import app

resultsappendages = dbc.Container([
    dbc.Col([
        dbc.Row(dbc.Col(html.H4('Results'))),
        dbc.Row([
            dbc.Col([
                html.P("""The main results are displayed below. First, you can view the evolutionary process in the first main plot. Colors will indicate how the individual evolved towards the optimal solution after each new generation. When hovering each individual, you can see the plot around updating with its value. The data includes also individuals that are not valid, and the constraints disrespected can be seen in the smaller plots below. The same plot also allows visualizing and understanding the Pareto frontier, in which further improvement is not possible."""),
            ], className = 'justify'),
            dbc.Col([
                html.P("""Besides that, a list with all the individuals generated is displayed in the following table. In this table, the user can sort the values combining ascending and descending sorting in each column. Another import asset is the parallel dimensions plot. It shows how the dimension set of the hull evolved throughout the optimization process. The concentration at one of the extremes may indicate space for further exploration."""),
            ], className = 'justify'),
        ]),
        html.Br(),
        dbc.Row(dbc.Col(html.H5('What do you want to view?'))),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='resultshullaxisy',
                    options=[
                        {'label': 'Average Velocity [knots]', 'value': 'AverageVelocity'},
                        {'label': 'Average Velocity Upwind [knots]', 'value': 'AverageVelocityUpwind'},
                        {'label': 'Comfort Ratio', 'value': 'Comfort'},
                    ],
                    value='AverageVelocity',
                    className='regularfont',
                ),
                html.Br()
            ]),
            dbc.Col([html.P('versus')], width=1, align='center'),
            dbc.Col([
                dcc.Dropdown(
                    id='resultshullaxisx',
                    options=[
                        {'label': 'Average Velocity [knots]', 'value': 'AverageVelocity'},
                        {'label': 'Average Velocity Upwind [knots]', 'value': 'AverageVelocityUpwind'},
                        {'label': 'Comfort Ratio', 'value': 'Comfort'},
                    ],
                    value='Comfort',
                    className='regularfont',
                ),
                html.Br()
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(dcc.Graph(id='output-optimization2')),
                html.A('Export all individuals generated', download='optimizationvpp.csv', href='assets/data/optimizationvpp.csv'),
            ], width=8),
        ]),
    ], className="mt-4")
])
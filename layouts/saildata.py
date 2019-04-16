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

from callbacks import saildataplots
from app import app

saildata = dbc.Container([
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
                        {'label': 'SA/DISP', 'value': 'SA/DISP'},
                        {'label': 'DISP/LWL', 'value': 'DISP/LWL'},
                        {'label': 'Comfort', 'value': 'Comfort'},
                        {'label': 'CapsizeRisk', 'value': 'CapsizeRisk'},
                        {'label': 'RollAcceleration', 'value': 'RollAcceleration'},
                        {'label': 'loa', 'value': 'loa'},
                        {'label': 'lwl', 'value': 'lwl'},
                        {'label': 'beam', 'value': 'beam'},
                        {'label': 'draft', 'value': 'draft'},
                        {'label': 'disp', 'value': 'disp'},
                        {'label': 'ballast', 'value': 'ballast'},
                        {'label': 'sa', 'value': 'sa'},
                    ],
                    value='Comfort',
                    className='regularfont',
                ),
                html.Br()
            ]),
            dbc.Col([html.P('versus')], width=1, align='center'),
            dbc.Col([
                dcc.Dropdown(
                    id='resultshullaxisx',
                    options=[
                        {'label': 'SA/DISP', 'value': 'SA/DISP'},
                        {'label': 'DISP/LWL', 'value': 'DISP/LWL'},
                        {'label': 'Comfort', 'value': 'Comfort'},
                        {'label': 'CapsizeRisk', 'value': 'CapsizeRisk'},
                        {'label': 'RollAcceleration', 'value': 'RollAcceleration'},
                        {'label': 'loa', 'value': 'loa'},
                        {'label': 'lwl', 'value': 'lwl'},
                        {'label': 'beam', 'value': 'beam'},
                        {'label': 'draft', 'value': 'draft'},
                        {'label': 'disp', 'value': 'disp'},
                        {'label': 'ballast', 'value': 'ballast'},
                        {'label': 'sa', 'value': 'sa'},
                    ],
                    value='lwl',
                    className='regularfont',
                ),
                html.Br()
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='rigtype',
                    options=[
                        {'label': 'Cutter', 'value': 'Cutter'},
                        {'label': 'Sloop', 'value': 'Sloop'},
                        {'label': 'Ketch', 'value': 'Ketch'}
                    ],
                    multi=True,
                    value="Cutter"
                ),
                dcc.Dropdown(
                    id='keeltype',
                    options=[
                        {'label': 'Steel', 'value': 'Steel'},
                        {'label': 'Fin Keel', 'value': 'FinKeel'},
                        {'label': 'Mono Keel', 'value': 'MonoKeel'}
                    ],
                    multi=True,
                    value="FinKeel"
                ),
            ]),
        ])
        dbc.Row([
            dbc.Col([
                html.Div(dcc.Graph(id='output-optimization-sd')),
                html.Br(),
                html.A('Export all individuals generated', download='saildata.csv', href='assets/data/saildata.csv'),
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label(Select the year interval),
                dcc.RangeSlider(
                    id='year-interval',
                    min=1960,
                    max=2000,
                    value=[1970, 1990],
                    marks={i for i in range(1970,2000)},
                    allowCross=False
                )
            ])
        ])
    ], className="mt-4")
])
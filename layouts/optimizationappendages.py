import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq
from app import app
from dash.dependencies import Input, Output, State
import json, codecs
import numpy as np

from callbacks import optimizationappendagescall

optimizationappendages = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Genetic Algorithm Configuration"),
            html.P("""The algorithm applied is the NSGA II - Nondominated Sorting Genetic Algorithm developed by Professor Kalyanmoy Deb. 
            It needs seven parameters to be configured. In case you are not familiar with them, more details are provided when hoving the 
            parameters or reading the documentation in the link below. In any case, the standard configuration will provide satisfactory results."""),
            dbc.Label("Method"),
            dcc.Dropdown(
                id='ga-method',
                options=[
                    {'label': 'NSGAII - Nondominated Sorting Genetic Algorithm', 'value': 'NSGAII'},
                    {'label': 'GDE3 - Generalized Differential Evolution', 'value': 'GDE3'},
                    {'label': 'OMOPSO - Multi-Objective Particle Swarm Optimization', 'value': 'OMOPSO'},
                    {'label': 'SMPSO - Speed-Constrained Particle Swarm Optimization', 'value': 'SMPSO'},
                    {'label': 'SPEA2 - Strength Pareto Evolutionary Algorithm', 'value': 'SPEA2'},
                    {'label': 'MOEA -  Multi-Objective Evolutionary Algorithm', 'value': 'EpsMOEA'},
                ],
                value='NSGAII',
                style={'width': '70%', 'font-size': '10pt'}
            ),
            dbc.Label("Number of offsprings"),
            dbc.Input(
                type='number', 
                id='offsprings-platypus', 
                value='300', 
                bs_size="sm", 
                style={'width': 80}
            ),
            html.Br(),
            dbc.Label("Behave of each algorithm"),
            html.Img(src='/assets/static/platypus3.png', width='100%'),
            html.Br(),html.Br(),html.Br(),
        ], className = "justify mt-4", md=6),
        dbc.Col([
            html.H4("Weighted Objectives"),
            html.P("""Now, instead of analysing the bare hul resistance, we will estimate the velocity through a VPP - Velocity Predictino Programme. The comfort is still analysed as second objective. As done before, chose the weight of velocity compared to comfort."""),
            dbc.Row([
                dbc.Col([
                    dbc.Label('Velocity'),
                    html.Div(id='resistance-weight-2', style={'display': 'inline-block'}),
                    daq.Knob(
                        id='weight1',
                        value=9,
                        min=0,
                        max=10,
                        scale={'start':0, 'interval': 1, 'labelInterval': 1},
                    ),
                ]),
                dbc.Col([
                    dbc.Label('Comfort Ratio Weight'),
                    html.Div(id='comfort-weight-2', style={'display': 'inline-block'}),
                    daq.Knob(
                        id='weight2',
                        value=6.5,
                        min=0,
                        max=10,
                        scale={'start':0, 'interval': 1, 'labelInterval': 1},
                    ),
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("True wind speed range analyzed in knots "),
                    dcc.RangeSlider(
                        id='wind-speed-range',
                        marks={
                            4: {'label': '4 kn'},
                            6: {'label': '6 kn'},
                            8: {'label': '8 kn'},
                            10: {'label': '10 kn'},
                            12: {'label': '12 kn'},
                            14: {'label': '14 kn'},
                            16: {'label': '16 kn'},
                            18: {'label': '18 kn'},
                            20: {'label': '20 kn'},
                            22: {'label': '22 kn'},
                        },
                        min=4,
                        max=22,
                        step=2,
                        value=[6, 16],
                    ),
                    html.Br(),html.Br(),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("True wind angle range analyzed"),
                    dcc.RangeSlider(
                        marks={i: '{}°'.format(i*10) for i in range(3, 19)},
                        min=3,
                        max=18,
                        value=[3, 18],
                        id='wind-angle-range',
                    ),
                    html.Br(),html.Br(),
                ])
            ]),
        ], className = "justify mt-4", md=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(), html.Br(),
            dbc.Label('Press the button below and wait for the confirmation', style={'align': 'center', 'text-align': 'center'}), html.Br(),
            html.Button(id='export-ga-2', type='submit', children='Run optimization'),
            html.Br(), html.Br(),
            html.Div(id='output-button-2'),
        ], className="update mt-4")
    ])
])
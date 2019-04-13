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

from callbacks import optimizationhullcall

optimizationhull = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Genetic Algorithm Configuration"),
            html.P("""The algorithm applied is the NSGA II - Nondominated Sorting Genetic Algorithm developed by Professor Kalyanmoy Deb. It needs seven parameters to be configured. In case you are not familiar with them, more details are provided when hoving the parameters or reading the documentation in the link below. In any case, the standard configuration will provide satisfactory results."""),
			html.Span(dbc.Label("Population size"), id="tooltip-population"),
            dbc.Tooltip("A set of individuals randomly generated to start the simulation.", target="tooltip-population"),
            dbc.Input(
                type='number', 
                id='pop-size', 
                value='10', 
                bs_size="sm", 
                style={'width': 80}),
            html.Span(dbc.Label("Number of offsprings"), id="tooltip-children"),
            dbc.Tooltip("The number of children to be produced at each generation as a result of crossover among its parents or mutation.", target="tooltip-children"),
            dbc.Input(
                type='number', 
                id='children-size', 
                value='4', 
                bs_size="sm", 
                style={'width': 80}),
            html.Span(dbc.Label("Maximum number of generations"), id="tooltip-generations"),
            dbc.Tooltip("The number of times parents will produce offsprings before an internal criteria are reached.", target="tooltip-generations"),
            dbc.Input(
                type='number', 
                id='max-generation', 
                value='15', 
                bs_size="sm", 
                style={'width': 80}),
            dbc.Label("Number of best fitting individuals selected"),
            dbc.Input(
                type='number', 
                id='halloffame-number', 
                value='5', 
                bs_size="sm", 
                style={'width': 80}),
            dbc.Label("Mutation probability for an offspring [%]"),
            dbc.Input(
                type='number', 
                id='mut-prob', 
                value='20', 
                bs_size="sm", 
                style={'width': 80}),
            dbc.Label("Independent probability for each attribute to be mutated [%]"),
            dbc.Input(
                type='number', 
                id='indpb-value', 
                value='20', 
                bs_size="sm", 
                style={'width': 80}),
            html.Span(dbc.Label("Crowding degree of the crossover [%]"), id="tooltip-crowding"),
            dbc.Tooltip("A high value will produce children resembling their parents, while a small value will produce solutions much more different.", target="tooltip-crowding"),
            dbc.Input(
                type='number', 
                id='eta_value', 
                value='20', 
                bs_size="sm", 
                style={'width': 80}),
            html.Br(),
            html.A('Read More about DEAP', href='https://deap.readthedocs.io/en/master/', target="_blank"),
            html.Br(), html.Br(),
			html.H4("Method of Selection"),
			dcc.Dropdown(
				id='ga-method', 
				options=[
					{'label': 'NSGA-II', 'value': '1'},
					{'label': 'SPEA-II', 'value': '2'},
				],
				placeholder='Choose one method for selecting the individuals',
				style={'width': '80%', 'font-size': '10pt'}
			),
			html.Br(),html.Br(),html.Br(),
        ], className = "justify mt-4", md=6),
		dbc.Col([
            html.H4("Weighted Objectives"),
            html.P("""Two objectives will be analyzed for the bare hull: resistance and comfort. The first is determined under different conditions of heel and velocity. The second is translated as a ratio between displacement, beam, and length. The objectives can be distinguished in terms of importance, which is proportional to its value. Besides that, in case you want to ignore an objective, set its value to zero."""),
            dbc.Row([
                dbc.Col([
					dbc.Label('Resistance Weight'),
                    html.Div(id='resistance-weight', style={'display': 'inline-block'}),
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
                    html.Div(id='comfort-weight', style={'display': 'inline-block'}),
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
                    dbc.Label("Velocities analyzed"),
                    dcc.RangeSlider(
                        id='velocity-range',
                        marks={i: '{} knots'.format(i) for i in range(2, 8)},
                        min=2,
                        max=7,
                        value=[3, 5],
                    ),
                    html.Br(),html.Br(),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Heel angles analyzed"),
                    dcc.RangeSlider(
                        marks={i: '{} deg'.format(i*10) for i in range(0, 6)},
                        min=0,
                        max=5,
                        value=[2, 3],
                        id='heel-range',
                    ),
                    html.Br(),html.Br(),
                ])
            ]),
            html.H4("Dimensions optimized"),
            html.P("""The limits of each dimension optimized at this stage can be set below. Standard values are recommended, but they can be stretched to explore more widely the dimensions space. The algorithm will evaluate which solutions are feasible and automatically exclude the ones that do not fit the criteria. Bear in mind that the values of minimum and maximum may affect performance and convergence. """),
            html.Div(id="dimensions-limits")
        ], className = "justify mt-4", md=6),
    ]),
	dbc.Row([
		dbc.Col([
			html.Br(), html.Br(),
			dbc.Label('Press the button below and wait for the confirmation', style={'align': 'center', 'text-align': 'center'}), html.Br(),
			html.Button(id='export-ga', type='submit', children='Run optimization'),
            html.Br(), html.Br(),
            html.Div(id='output-button'),
		], className="update mt-4")
	])
])

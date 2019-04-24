import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import numpy as np

from callbacks import optimizationhullcall

optimizationhull = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4('Genetic Algorithm Configuration'),
            html.P("The algorithm applied is the NSGA II - Nondominated Sorting Genetic Algorithm developed by Professor Kalyanmoy Deb. It needs seven parameters to be configured. In case you are not familiar with them, more details are provided when hoving the parameters or reading the documentation in the link below. In any case, the standard configuration will provide satisfactory results."),
            dcc.Dropdown(
                id='type-optimization',
                options=[
                    {'label': 'Default methods', 'value': 'default'},
                    {'label': 'Personalized configuration', 'value': 'custom'},
                ],
                value='default',
                style={'width': '70%', 'font-size': '10pt'}
            ),
			html.Br(), html.Br(),
			html.H4("Optimization Parameters"),
            html.Div(id="option-optimization"),
            html.Br(), html.Br(), 
            html.H4("Constraints"),
            html.P("Constraints help maintain the sailboats feasible. They evaluate safety the Capsize Screening Factor, that empirically evaluate the likelihood of capsizing."),
			html.Img(src='/assets/static/cs.png', height='28pt'),
			html.Br(),html.Br(),
			dbc.Label("Capsize Screening Factor"),
			dbc.Input(
                type='number', 
                id='capsize-factor', 
                value='2', 
                bs_size="sm", 
                style={'width': 80}),
			html.Div(id="disp-tc-min")
        ], className = "justify mt-4", md=6),
        dbc.Col([
            html.H4("Weighted Objectives"),
            html.P("""Two objectives will be analyzed for the bare hull: resistance and comfort. The first is determined under different conditions of heel and velocity. The second is translated as a ratio between displacement, beam, and length. The objectives can be distinguished in terms of importance, which is proportional to its value. Besides that, in case you want to ignore an objective, set its value to zero."""),
            dbc.Row([
                dbc.Col([
                    html.Div(id='resistance-weight', style={'display': 'block', 'text-align': 'center'}),
                    daq.Knob(
                        id='weight1',
                        value=9,
                        min=0,
                        max=10,
                        scale={'start':0, 'interval': 1, 'labelInterval': 1},
						style={'display': 'block', 'text-align': 'center'}
                    ),
                ]),
                dbc.Col([
                    html.Div(id='comfort-weight', style={'display': 'block', 'text-align': 'center'}),
                    daq.Knob(
                        id='weight2',
                        value=6.5,
                        min=0,
                        max=10,
                        scale={'start':0, 'interval': 1, 'labelInterval': 1},
						style={'display': 'block', 'text-align': 'center'}
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
			html.Br(),
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

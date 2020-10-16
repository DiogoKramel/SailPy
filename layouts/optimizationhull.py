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
            html.P("The optimizaton method can be choosen between a default method, in which all the parameters are automatically\
                 set based on the literature best recommendations, and a custom method. The latter applies the algorithm NSGA II \
                 - Nondominated Sorting Genetic Algorithm developed by Professor Kalyanmoy Deb. It needs seven parameters to\
                 be configured. In case you are not familiar with them, more details are provided when hoving the parameters \
                 or reading the documentation in the link below. In any case, the standard configuration will provide satisfactory results."),
            #dcc.Dropdown(
            #    id='type-optimization',
            #    options=[
            #        {'label': 'Default methods', 'value': 'default'},
            #        {'label': 'Personalized configuration', 'value': 'custom'},
            #    ],
            #    value='default',
            #    style={'width': '70%', 'font-size': '10pt'}
            #),
			#html.Br(), html.Br(),
			html.H4("Optimization Parameters"),
            #html.Div(id="option-optimization"),
            html.Div([
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
            ]),
            html.Br(), html.Br(), 
            html.H4("Constraints"),
            html.P("Constraints help maintain the sailboats feasible. The Capsize Screening Factor empirically evaluates the likelihood of capsizing based on the formula shown below. Another constraint is the displacement, which assits the optimization process on not allowing unrealistic hulls."),
			html.Img(src='/assets/static/cs.png', height='28pt'),
			html.Br(),html.Br(),
			dbc.Label("Capsize Screening Factor"),
			dbc.Input(
                type='number', 
                id='capsize-factor', 
                value='2', 
                bs_size="sm", 
                style={'width': 80}),
        ], className = "justify mt-4", md=6),
        dbc.Col([
            html.H4("Weighted Objectives"),
            html.P("""Two objectives will be analyzed for the bare hull: resistance and added resistance in waves. They are determined under different conditions of \
                heel and velocity that the user can set through the sliders below. The objectives can be distinguished in terms of importance, which is proportional \
                to its value. Besides that, in case you want to ignore an objective, set its value to zero."""),
            dbc.Row([
                dbc.Col([
                    html.Div(id='resistance-weight', style={'display': 'block', 'text-align': 'center'}),
                    dcc.Slider(
                        id='weight1',
                        value=5,
                        min=0,
                        max=10,
                        marks={0: '0', 2: '2', 4: '4', 6: '6', 8: '8', 10: '10'},
                    ),
                ]),
                dbc.Col([
                    html.Div(id='added-weight', style={'display': 'block', 'text-align': 'center'}),
                    dcc.Slider(
                        id='weight2',
                        value=5,
                        min=0,
                        max=10,
                        marks={0: '0', 2: '2', 4: '4', 6: '6', 8: '8', 10: '10'},
                    ),
                ]),
            ]),
            html.Br(), html.Br(),
            html.H4("Study case"),
            html.P("""THe parameters below describe the expected operational profile of the boat and the expected sea conditions."""),
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
            dbc.Row([
                dbc.Col([
                    dbc.Label("Wave height"),
                    dcc.RangeSlider(
                        id='height_range',
                        marks={i: '{} m'.format(i) for i in range(0, 6)},
                        min=0,
                        max=5,
                        value=[1, 3],
                    ),
                    html.Br(),html.Br(),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Wave angle"),
                    dcc.RangeSlider(
                        id='angle_range',
                        marks={i: '{} deg'.format(i) for i in range(100, 181, 20)},
                        min=100,
                        max=180,
                        value=[120, 160],
                    ),
                    html.Br(),html.Br(),
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Wave length as fraction of ship length"),
                    dcc.RangeSlider(
                        id='length_range',
                        marks={0.5: '0.5', 1.0: '1.0', 1.5: '1.5', 2.0: '2.0', 2.5: '2.5', 3.0: '3.0', 3.5: '3.5', 4.0: '4.0'},
                        min=0.5,
                        max=4,
                        value=[1, 1.5],
                    ),
                    html.Br(),html.Br(),
                ])
            ]),
			html.Br(),
            html.H4("Dimensions optimized"),
            html.P("""The limits of each dimension optimized at this stage can be set below. Standard values are recommended, \
                but they can be stretched to explore more widely the dimensions space. The algorithm will evaluate which \
                solutions are feasible and automatically exclude the ones that do not fit the criteria. Bear in mind that \
                the values of minimum and maximum may affect performance and convergence. """),
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

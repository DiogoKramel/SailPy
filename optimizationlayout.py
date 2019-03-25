import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq

import optimizationhullcallbacks

optimizationhull = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Genetic Algorithm Configuration"),
            html.P("""The algorithm is the NSGA II - Nondominated Sorting Genetic Algorithm and needs seven parameters to be configures. In case you are not familiar with that, detail are provided when hoving the parameters or you can find more in the link below. In any case, the standard configuration will provide satisfactory results."""),
            html.Span(dbc.Label("Population size"), id="tooltip-population"),
            dbc.Tooltip("The number of individuals to start the simulations with.", target="tooltip-population"),
            dbc.Input(
				type='number', 
				id='pop-size', 
				value='10', 
				bs_size="sm", 
				style={'width': 80}),
            html.Span(dbc.Label("Children size"), id="tooltip-children"),
            dbc.Tooltip("The number of children to produce at each generation.", target="tooltip-children"),
            dbc.Input(
				type='number', 
				id='children-size', 
				value='4', 
				bs_size="sm", 
				style={'width': 80}),
            dbc.Label("Maximum number of generations"),
            dbc.Input(
				type='number', 
				id='max-generation', 
				value='15', 
				bs_size="sm", 
				style={'width': 80}),
            dbc.Label("Mutation probabitily [%]"),
            dbc.Input(
				type='number', 
				id='mut-prob', 
				value='20', 
				bs_size="sm", 
				style={'width': 80}),
            dbc.Label("Number of best fitting individuals selected"),
            dbc.Input(
				type='number', 
				id='halloffame-number', 
				value='5', 
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
            dbc.Tooltip("A high value will produce children resembling to their parents, while a small value will produce solutions much more different.", target="tooltip-crowding"),
            dbc.Input(
				type='number', 
				id='eta_value', 
				value='20', 
				bs_size="sm", 
				style={'width': 80}),
            html.Br(),
            html.A('Read More about DEAP', href='https://deap.readthedocs.io/en/master/', target="_blank"),
            html.Br(), html.Br()
        ], md=6),

        dbc.Col([
			html.H2("Weighted Objectives"),
            html.P("""The objectives can be distinguished in terms of importance, which translates to the higher the value, the more prioritized the objective will be. Besides that, it is possible the set wheter minimize (negative values), maximize (positive), or ignore (zero)."""),
            dbc.Row([
                dbc.Col([
					dbc.Label("Total Hull Resistance"),
                    html.Div(id='weight1-value', style={'display': 'inline-block', 'font-size': '10pt'}),
                    daq.Knob(
                        id='weight1',
                        value=-0.9,
                        min=-1,
                        max=1,
                        scale={'start':-1, 'interval': 0.25, 'labelInterval': 0.5},
                    ),
                ]),
                dbc.Col([
					dbc.Label("Comfort Ratio"),
                    html.Div(id='weight2-value', style={'display': 'inline-block', 'font-size': '10pt'}),
                    daq.Knob(
                        id='weight2',
                        value=0.7,
                        min=-1,
                        max=1,
                        scale={'start':-1, 'interval': 0.25, 'labelInterval': 0.5},
                    ),
                ]),
            ]),
			dbc.Row([
				dbc.Col([
					dbc.Label("Velocities analysed"),
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
					dbc.Label("Heel analysed"),
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
            html.H2("Dimensions optimized"),
            html.P("""In this last stage, the dimensions to be optimized can be toogled among the options below. Bear in mind that the size of minimum and maximum limits will affect performance (and processing time). """),
            html.Div(id="dimensions-chosen-optimization")
        ], md=6),
    ]),
    dbc.Row([
        dbc.Col([
            html.Br(), html.Br(),
            dbc.Button(dcc.Link("Run optimization",style={'color': 'white'}), id="export-ga"),
			html.Br(), html.Br(),
			html.P(id='output-container-button'),
            html.Br(), html.Br(),
        ], style={'textAlign': 'center'}),
    ]),
], className="mt-4"),
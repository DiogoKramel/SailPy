import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input

from callbacks import resultshullplots
from app import app

resultshull = dbc.Container([
    dbc.Col([
        dbc.Row(dbc.Col(html.H4('Results'))),
        dbc.Row([
            dbc.Col([
                html.P("The main results are displayed below. First, you can view the evolutionary process in the first main plot. Colors will indicate how the individual evolved towards the optimal solution after each new generation. When hovering each individual, you can see the plot around updating with its value. The data includes also individuals that are not valid, and the constraints disrespected can be seen in the smaller plots below. The same plot also allows visualizing and understanding the Pareto frontier, in which further improvement is not possible."),
            ], className = 'justify'),
            dbc.Col([
                html.P("Besides that, a list with all the individuals generated is displayed in the following table. In this table, the user can sort the values combining ascending and descending sorting in each column. Another import asset is the parallel dimensions plot. It shows how the dimension set of the hull evolved throughout the optimization process. The concentration at one of the extremes may indicate space for further exploration."),
            ], className = 'justify'),
        ]),
        html.A('Export all individuals generated', download='optimizationresistance.csv', href='assets/data/optimizationresistance.csv'),
        html.Br(), html.Br(),
        dbc.Row(dbc.Col(html.H5('What do you want to view?'))),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='resultshullaxisy',
                    options=[
                        {'label': 'Resistance', 'value': 'Resistance'},
                        {'label': 'Comfort Ratio', 'value': 'Comfort'},
                        {'label': 'Waterline length', 'value': 'LWL'},
                        {'label': 'Waterline beam', 'value': 'BWL'},
                        {'label': 'Draft', 'value': 'Draft'},
                        {'label': 'Displacement', 'value': 'Displacement'},
                        {'label': 'Waterplane area', 'value': 'AWP'},
                        {'label': 'LCB', 'value': 'LCB'},
                        {'label': 'LCF', 'value': 'LCF'},
                    ],
                    value='Resistance',
                    className='regularfont',
                ),
            ]),
            dbc.Col([html.P('versus')], width=1, align='center'),
            dbc.Col([
                dcc.Dropdown(
                    id='resultshullaxisx',
                    options=[
                        {'label': 'Resistance', 'value': 'Resistance'},
                        {'label': 'Comfort Ratio', 'value': 'Comfort'},
                        {'label': 'Waterline length', 'value': 'LWL'},
                        {'label': 'Waterline beam', 'value': 'BWL'},
                        {'label': 'Draft', 'value': 'Draft'},
                        {'label': 'Displacement', 'value': 'Displacement'},
                        {'label': 'Waterplane area', 'value': 'AWP'},
                        {'label': 'LCB', 'value': 'LCB'},
                        {'label': 'LCF', 'value': 'LCF'},
                    ],
                    value='Comfort',
                    className='regularfont',
                ),
            ]),
        ]),
		html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(dcc.Graph(id='output-optimization')),
				html.H4('Select one individual'),
				html.P("Among all the individuals generated throughout the optimization proccess, select one below. The table above and the Pareto Frontier will help you to find the specific hull number, equivalent to the individual ID, that fits your needs."),
				html.Div(id='export-hull-dimensions')
            ], width=10),
            dbc.Col(html.Div(dcc.Graph(id='plot-resistance-individual')), width=2),
        ]),
		dbc.Row([
			dbc.Col([
				dbc.Label('SAC angle at the bow [degrees]'),
				dbc.Input(type='text', id='alpha_f_sac2', bs_size='sm', value=5, style={'width': '75%'}),
				dbc.Label('SAC angle at the stern [degrees]'),
				dbc.Input(type='text', id='alpha_i_sac2', bs_size='sm', value=15, style={'width': '75%'}),
				dbc.Label('Hull bottom angle [degrees]'),
				dbc.Input(type='text', id='beta_n2', bs_size='sm', value=0, style={'width': '75%'})
			], md=4),
			dbc.Col([
				html.Div(dcc.Graph(id='insert-section-choosen'))
			], md=8)
		]),
        html.Br(),
		html.Details([
			html.Summary('Constraints Analysis'),
			dbc.Row([
				dbc.Col([html.Div(dcc.Graph(id='plot-limits-lwl-bwl'))]),
				dbc.Col([html.Div(dcc.Graph(id='plot-limits-bwl-tc'))]),
			]),
			dbc.Row([
				dbc.Col([html.Div(dcc.Graph(id='plot-limits-lwl-disp'))]),
				dbc.Col([html.Div(dcc.Graph(id='plot-limits-awp-disp')),]),
			]),
			dbc.Row(html.Div(id='plot-constraints-count')),
		]),
		html.Details([
			html.Summary('Parallel Plot'),
			dcc.Dropdown(
					id='parallel-datatype', 
					options=[
						{'label': 'All individuals', 'value': 1},
						{'label': 'Only valid individuals', 'value': 2},
						{'label': 'Only not valid individuals', 'value': 3},
					],
					value='1',
					style={'width': '300pt'},
					className='regularfont',
			),
			html.Div(dcc.Graph(id='plot-parallel-dimensions')),
		]),
		html.Details([
			html.Summary('Data of all individuals'),
			dbc.Row(
				dbc.Col([
					html.P("All the valid individuals are listed below. By reordering the columns, the hulls with least resistance or displacement can be found. When selected, the following plots will be automatically update ith their position in the optimization course."),
					html.Div(id='table-all-individuals'),
				])
			),
			html.Br(),
			dbc.Row(dbc.Col(html.Div(id='plot-dimensions'))),
		]),
    ], className='mt-4')
])
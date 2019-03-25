import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq
import dash_table
import pandas as pd

import resultsplots

resultshull = dbc.Container([
    dbc.Col([
        dbc.Row(dbc.Col(html.H2("Results"))),
        dbc.Row([
            dbc.Col([
                html.P("""The main results are displayed below. First, you can view the evolutionary process described in the objectives plot. Colors will indicate how the individual evolved towards the optimal solution. The same plot also allows to perceive any paretro-frontiers, in which improvement is not possible."""),
            ]),
            dbc.Col([
                html.P("""Besides that, a list with all the individuals generated is displayed in the following table. Below this table, the evolutionary tree for the best individual is shown to illustrate the effectiveness of the method. You can also find the how the dimensionions are connected and the dominator and dominance plot."""),
            ]),
            
        ]),
		html.Br(),
        dbc.Row(dbc.Col(html.H4("What do you want to view?"))),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='resultshullaxisy',
                    options=[
                        {'label': 'Resistance', 'value': "Resistance"},
						{'label': 'Comfort Ratio', 'value': "Comfort"},
                        {'label': 'Waterline length', 'value': "LWL"},
                        {'label': 'Waterline beam', 'value': "BWL"},
                        {'label': 'Draft', 'value': "Draft"},
                        {'label': 'Displacement', 'value': "Displacement"},
                        {'label': 'Waterplane area', 'value': "AWP"},
                        {'label': 'LCB', 'value': "LCB"},
                        {'label': 'LCF', 'value': "LCF"},
                    ],
                    value="Resistance",
					className="regularfont",
                ),
                html.Br()
            ]),
            dbc.Col([html.P("versus")], width=1, align="center"),
            dbc.Col([
                dcc.Dropdown(
                    id='resultshullaxisx',
                    options=[
                        {'label': 'Resistance', 'value': "Resistance"},
						{'label': 'Comfort Ratio', 'value': "Comfort"},
                        {'label': 'Waterline length', 'value': "LWL"},
                        {'label': 'Waterline beam', 'value': "BWL"},
                        {'label': 'Draft', 'value': "Draft"},
                        {'label': 'Displacement', 'value': "Displacement"},
                        {'label': 'Waterplane area', 'value': "AWP"},
                        {'label': 'LCB', 'value': "LCB"},
                        {'label': 'LCF', 'value': "LCF"},
                    ],
                    value="Comfort",
					className="regularfont",
                ),
                html.Br()
            ]),
        ]),
        dbc.Row([
			dbc.Col(
				html.Div(dcc.Graph(id='output-optimization')), width=10
				),
			dbc.Col(
				html.Div(dcc.Graph(id='plot-resistance-individual')), width=2
			),
		]),
		html.Br(),
		dbc.Row([
			
			dbc.Col(
				html.Div(dcc.Graph(id='plot-limits-lwl-bwl')), width=3
			),
			dbc.Col(
				html.Div(dcc.Graph(id='plot-limits-bwl-tc')),
			),
			dbc.Col(
				html.Div(dcc.Graph(id='plot-limits-lwl-disp'))
			),
			dbc.Col(
				html.Div(dcc.Graph(id='plot-limits-awp-disp'))
			),
		]),
    ], className="mt-4")
])

df = pd.read_csv("data/optimizationresistance.csv")
datatable = pd.read_csv("data/optimizationresistance.csv")
datatable = datatable.loc[datatable['valid']==True]
datatable = datatable.loc[:,"id":"LCB"]

resultsplus = dbc.Container([
    dbc.Col([
		dbc.Row(dbc.Col(html.H4("Dimensions Parallel Plot"))),
		dbc.Row(dbc.Col(html.Div(dcc.Graph(id='plot-parallel-dimensions')))),
		html.Br(),
		dbc.Row(dbc.Col([
			html.H4("List of all individuals"),
			dash_table.DataTable(
				id='datatable-interactivity',
				columns=[{"name": i, "id": i, "deletable": True} for i in datatable.columns],
				data=datatable.to_dict("rows"),
				#editable=True,
				sorting=True,
				sorting_type="multi",
				#row_deletable=True,
				selected_rows=[],
				pagination_mode="fe",
				pagination_settings={
					"displayed_pages": 1,
					"current_page": 0,
					"page_size": 10,
				},
				navigation="page",
    		)],
		)),
		html.Br(),
		dbc.Row(dbc.Col(html.H4("Select and individual"))),
		dbc.Row([
			dcc.Dropdown(
				id='dropdown', 
				options=[
					{'label': "Hull #{}".format(i), 'value': i} for i in df.index.unique()
				],
				placeholder='Select one hull to be optimised',
				style={'width': '100%'}),
				html.Br(),html.Br(),html.Br(),
		]),
		
		#dbc.Row(dbc.Col(html.H4("Genealogy"))),
		#dbc.Row(
		#	dbc.Col(html.Details([
		#		html.Img(src="assets/network.png", height="400px")
		#	])
		#)),
		#html.Br(),

		
		dbc.Row([
			html.Br(),html.Br(),
			dbc.Button(
				dcc.Link("< Start again", href=f"/parametrichull", style={'color': 'white'})),
			dbc.Button(
				dcc.Link("Optimize appendages >", href=f"/appendage", style={'color': 'white'})),
			html.Br(), html.Br()
		], justify="center"),
		
    ], className="mt-4")
])


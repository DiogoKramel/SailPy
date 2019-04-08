import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_daq as daq
import dash_table
import pandas as pd

from callbacks import resultshullplots
from app import app

resultshull = dbc.Container([
    dbc.Col([
        dbc.Row(dbc.Col(html.H2("Results"))),
        dbc.Row([
            dbc.Col([
                html.P("""The main results are displayed below. First, you can view the evolutionary process in the first main plot. Colors will indicate how the individual evolved towards the optimal solution. It includes individuals that are not valid, and the constraint disrespected can be seen in the smaller plots below. The same plot also allows visualizing and understanding the Pareto frontier, in which further improvement is not possible."""),
            ], className = "justify"),
            dbc.Col([
                html.P("""Besides that, a list with all the individuals generated is displayed in the following table. In this table, the user can sort the values combining ascending and descending sorting in each column. Another import asset is the parallel dimensions plot. It shows how the dimension set of the hull evolved throughout the optimization process. The concentration at one of the extremes may indicate space for further exploration."""),
            ], className = "justify"),
        ]),
		html.Br(),
		dbc.Row(
			dbc.Col(
				html.Div(html.A('Export all individuals generated', download='optimizationresistance.csv', href='assets/data/optimizationresistance.csv'))
			)
		),
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
			dbc.Col(html.Div(dcc.Graph(id='output-optimization')), width=10),
			dbc.Col(html.Div(dcc.Graph(id='plot-resistance-individual')), width=2),
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
		html.Br(), 
		html.Br(),
    ], className="mt-4")
])


df = pd.read_csv("assets/data/optimizationresistance.csv")
datatable = pd.read_csv("assets/data/optimizationresistance.csv")
datatable = datatable.loc[datatable['valid']==True]
datatable = datatable.loc[:,"id":"LCB"]

resultsplus = dbc.Container([
    dbc.Col([
		dbc.Row(dbc.Col(html.H4("Dimensions Parallel Plot"))),
		dbc.Row(dbc.Col(html.Div(dcc.Graph(id='plot-parallel-dimensions')))),
		html.Br(),

		dbc.Row(dbc.Col([
			html.H4("List of all individuals"),
			html.Div(
			dash_table.DataTable(
				id='datatable-interactivity',
				columns=[{"name": i, "id": i, "deletable": True} for i in datatable.columns],
				data=datatable.to_dict("rows"),
				editable=True,
				sorting=True,
				sorting_type="multi",
				row_selectable="multi",
				row_deletable=True,
				selected_rows=[],
				#n_fixed_rows=1,
				pagination_mode="fe",
				pagination_settings={
					"displayed_pages": 1,
					"current_page": 0,
					"page_size": 10,
				},
				navigation="page",
    		),
		)])),
		#html.Br(),
		#dbc.Row(dbc.Col(
		#	html.Div(id="plot-dimensions"),
		#)),

		html.Br(),
		dbc.Row(dbc.Col(html.H4("Select one individual"))),
		dbc.Row([
			dcc.Dropdown(
				id='dropdown-hull-dimensions', 
				options=[
					{'label': "Hull #{}".format(i), 'value': i} for i in df.index.unique()
				],
				value='1',
				placeholder='Select one hull to be optimised in the next phase',
				style={'width': '100%', 'font-size': '10pt'}
			),
		]),
		html.Br(),
		#dbc.Row([
		#	html.Br(),html.Br(),
		#	dbc.Button(dcc.Link("Start again", href=f"/parametrichull", style={'color': 'white'})),
		#	html.P(" ", style={'display': 'inline-block', 'padding': '10px'}),
		#	dbc.Button(dcc.Link("Optimize appendages", href=f"/appendage", style={'color': 'white'})),
		#], justify="center"),
	html.Br(), html.Br(),html.Br(), html.Br(),html.Br(),
    ], className="mt-4")
])
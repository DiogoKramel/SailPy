import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq
import pandas as pd
import numpy as np

from callbacks import dimensionsappendagescall, dimensionsappendagesplots

dimensions = pd.read_csv("data/initialhull.csv")
lwl = np.float(min(dimensions["LWL"]))
bwl = np.float(min(dimensions["BWL"]))
disp = np.float(min(dimensions["Displacement"]))
tc = np.float(min(dimensions["Draft"]))
lcb = np.float(min(dimensions["LCB"]))
lcf = np.float(min(dimensions["LCF"]))

appendages = dbc.Container([
	dbc.Row(
		dbc.Col(
			html.H2("Dimensions")
		),
	),
	dbc.Row([
        dbc.Col([
			html.P("After optimizing the the hull main dimensions, in this phase we will concentrate in stablishing the dimensions for the rudder, keel and sails in order to improve its overall performance. At this page, you have the dimensions of the hull you selected before. You can change them, but have in mind it can cause an unfeasible vessel or decrease its performance."),
			html.P("Below, you will find the dimensions necessary for running the VPP - Velocity Prediction Program. In order to ease the prelimnary setup, regressions based on the hull main dimensions were applied to estimated them. However, you are encouraged to investigate and adapt them to your needs. You can see how they affect the sailboat by looking at the dynamic profile on the right side. Bear in mind that they depend on one another."),
		], className = "justify"),
		dbc.Col([
			dbc.Row([
				dbc.Col([
					dbc.Label("Waterline length [m]"),
					dbc.Input(type='text', id='lwl-new', bs_size="sm", value=format(round(lwl,2))),
					dbc.Label("Waterline beam [m]"),
					dbc.Input(type='text', id='bwl-new', bs_size="sm", value=round(bwl,2)),
					dbc.Label("Draft [m]"),
					dbc.Input(type='text', id='tc-new', bs_size="sm", value=format(round(tc,2))),
				]),
				dbc.Col([
					dbc.Label("Displacement [m3]"),
					dbc.Input(type='text', id='disp-new', bs_size="sm", value=format(round(disp,2))),
					dbc.Label("LCB [m]"),
					dbc.Input(type='text', id='lcb-new', bs_size="sm", value=format(round(lcb,2))),
					dbc.Label("LCF [m]"),
					dbc.Input(type='text', id='lcf-new', bs_size="sm", value=format(round(lcf,2))),
				]),
			])
		]),
	]),
	html.Br(),
	html.Div(id="save-new-dim", style={'display': 'none'}),
	dbc.Row([
		dbc.Col([
			html.H4("Hull"),
			html.Div(id='dimensions-hull'),
			html.Br(),
			html.H4("Sail"),
			dbc.Label("Sail configuration"),
			dcc.Dropdown(
				id='sailset',
				options=[
					{"label": "Main sail and jib", "value": '1'},
					{"label": "Main sail and spinnaker", "value": '2'},
					{"label": "Main sail, jib, and spinnaker", "value": '3'},
					{"label": "Main sail only", "value": '4'},
				],
				value='1',
				placeholder='Choose one saill plan',
				style={'width': '100%', 'font-size': '10pt'},
			),
			html.Div(id='dimensions-sail'),
		], width=3),
		dbc.Col([
			html.H4("Rudder"),
			html.Div(id='dimensions-rudder'),
			html.Br(),
			html.H4("Keel"),
			html.Div(id='dimensions-keel'),
		], width=3),
		dbc.Col([
			html.H4("Side plan view"),
            html.Div(dcc.Graph(id='plot-appendages', style={'width': 'inherit'})),
			html.Br(),
			#html.Div(id="dimension-loa"),
			html.Br(),html.Br(),html.Br(),html.Br(),html.Br()
		], width=6),
	]),
	html.Br(),html.Br(),
	dbc.Row([
		dbc.Button(dcc.Link("Go back", href=f"/parametrichull", style={'color': 'white'})),
		html.P(" ", style={'display': 'inline-block', 'padding': '10px'}),
		dbc.Button(dcc.Link("Set optimization parameters", href=f"/optimizationappendages", style={'color': 'white'})),
	], justify="center"),
	html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
], className="mt-4",)


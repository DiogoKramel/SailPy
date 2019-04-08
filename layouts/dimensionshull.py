import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq

from callbacks import dimensionshullcall
from callbacks import dimensionshullplots

hull = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Main parameters"),
            html.P("""Set the category and length that will serve as the basis to build the regressions for the primary and secondary dimensions found below. You can follow how your choices affect the hull through the plots."""),
            dbc.FormGroup([
                dbc.Label("Category"),
                dbc.RadioItems(
                    id='boat-category',
                    options=[
                        {"label": "Cruiser", "value": 'cruiser'},
                        {"label": "Racer", "value": 'racer'},
                    ],
                    value='cruiser',
                    inline=True,
                    className="regularfont"
                ),
                html.Br(),
                dbc.Label("Overall lengt"),
                html.Div(id='output-loa', style={'display': 'inline-block'}),
                dcc.Slider(
                    id='loa',
                    min=20,
                    max=50,
                    value=40,
                    step=1,
                    marks={20: '20ft', 25: '25ft', 30: '30ft', 35: '35ft', 40: '40ft', 45: '45ft', 50: '50ft'},
                ),
                html.Br(),
            ]),
            html.Div(id="output-primary", style={'width': '50%'}),
            html.Div(id="output-secondary"),
            html.Div(id="output-tertiary", style={'width': '50%'}),
            html.Br(), html.Br(), html.Br(),
        ], className = "justify", md=4),
        dbc.Col([
            html.H4("Lines Drawing"),
            html.Div(dcc.Graph(id='insert-sac', style={'width': 'inherit'})),
            html.Br(),
            html.Div(dcc.Graph(id='insert-wl', style={'width': 'inherit'})),
            html.Br(),
            html.Div(dcc.Graph(id='insert-keel', style={'width': 'inherit'})),
            html.Br(),
            html.Div(dcc.Graph(id='insert-section', style={'width': 'inherit'})),
            html.Br(),
            html.H4("Testing fitness"),
            html.H5("DELFT Series"),
            html.Div(id='output-bwlsac', style={'display': 'none'}),
            html.Div(id="output-lwlbwl", className="regularfont"),
            html.Div(id="output-bwltc", className="regularfont"),
            html.Div(id="output-lwldisp", className="regularfont"),
            html.Div(id="output-loadingfactor", className="regularfont"),
            html.Div(id="output-prismatic", className="regularfont"),
            html.H5("Other evaluations"),
            html.Div(id="output-conc", className="regularfont"),
            html.Br(),
            html.Div(id="output-feasibility"),
        ], className = "justify", md=8)
    ]),
    html.Br(), html.Br(),html.Br(), html.Br(),html.Br(),
    #dbc.Row([
    #    dbc.Col([
    #        html.Br(),
    #        html.Div(id='output-submit-dimensions',
    #                 children='Enter a value and press submit', style={'display': 'none'}),
    #        dbc.Button(dcc.Link("Submit dimensions and calculate preliminary results",
    #                            href=f"/optimizationhull", style={'color': 'white'}), id="export-dimensions"),
    #    ], width=5),
    #], justify="center"),
], className="mt-4",)

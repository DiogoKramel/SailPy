import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq
import pandas as pd
import numpy as np
import json, codecs

from callbacks import dimensionsappendagescall, dimensionsappendagesplots


appendages = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H4("Dimensions")
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
                    dbc.Input(type='text', id='lwl-new', bs_size="sm", value=format(round(json.loads(codecs.open('assets/data/dimensions-hull.json', 'r', encoding='utf-8').read())["lwl"],2))),
                    dbc.Label("Waterline beam [m]"),
                    dbc.Input(type='text', id='bwl-new', bs_size="sm", value=format(round(json.loads(codecs.open('assets/data/dimensions-hull.json', 'r', encoding='utf-8').read())["bwl"],2))),
                    dbc.Label("Draft [m]"),
                    dbc.Input(type='text', id='tc-new', bs_size="sm", value=format(round(json.loads(codecs.open('assets/data/dimensions-hull.json', 'r', encoding='utf-8').read())["tc"],2))),
                ]),
                dbc.Col([
                    dbc.Label("Displacement [m3]"),
                    dbc.Input(type='text', id='disp-new', bs_size="sm", value=format(round(json.loads(codecs.open('assets/data/dimensions-hull.json', 'r', encoding='utf-8').read())["disp"],2))),
                    dbc.Label("LCB [m]"),
                    dbc.Input(type='text', id='lcb-new', bs_size="sm", value=format(round(json.loads(codecs.open('assets/data/dimensions-hull.json', 'r', encoding='utf-8').read())["lcb"],2))),
                    dbc.Label("LCF [m]"),
                    dbc.Input(type='text', id='lcf-new', bs_size="sm", value=format(round(json.loads(codecs.open('assets/data/dimensions-hull.json', 'r', encoding='utf-8').read())["lcf"],2))),
                ]),
            ])
        ]),
    ]),
    html.Br(),
    html.Div(id="save-new-dim", style={'display': 'none'}),
    dbc.Row([
        dbc.Col([
            html.H5("Hull"),
            dbc.Label("Free Board [m]"), html.Br(),
            dbc.Input(type='text', id='freeboard-min', bs_size="sm", value=format(round(1,2)), className='boxminimum'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='freeboard', bs_size="sm", value=format(round(1.3,2)), className='boxinput'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='freeboard-max', bs_size="sm", value=format(round(1.6,2)), className='boxmaximum'),

            html.Div(id="dimension-boa"),
            dbc.Label("Overhang [m]"), html.Br(),
            dbc.Input(type='text', id='overhang-min', bs_size="sm", value=format(round(0.5,2)), className='boxminimum'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='overhang', bs_size="sm", value=format(round(1,2)), className='boxinput'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='overhang-max', bs_size="sm", value=format(round(1.5,2)), className='boxmaximum'),

            dbc.Label("Bow angle [deg]"), html.Br(),
            dbc.Input(type='text', id='bowangle-min', bs_size="sm", value=format(round(0,2)), className='boxminimum'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='bowangle', bs_size="sm", value=format(round(15,2)), className='boxinput'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='bowangle-max', bs_size="sm", value=format(round(30,2)), className='boxmaximum'),
            html.Br(),html.Br(),
            
            html.H5("Sail"),
            dbc.Label("Sail configuration"),
            dcc.Dropdown(
                id='sailset',
                options=[
                    {"label": "Sloop: Mainsail and foresail", "value": '1'},
                    {"label": "Cat: Mainsail and spinnaker", "value": '2'},
                    {"label": "Cutter: Mainsail, foresail, and spinnaker", "value": '3'},
                    {"label": "Cat: Mainsail only", "value": '4'},
                ],
                value='1',
                placeholder='Choose one saill plan',
                style={'width': '100%', 'font-size': '10pt'},
            ),
            html.Div(id='dimensions-sail'),
            dbc.Label("Mizzen"),
            dcc.Dropdown(
                id='mzn-check',
                options=[
                    {"label": "Do not include", "value": '0'},
                    {"label": "Include", "value": '1'},
                ],
                value='0',
                style={'width': '100%', 'font-size': '10pt'},
            ),
            html.Div(id='dimensions-mizzen')
        ], width=3),
        dbc.Col([
            html.H5("Rudder"),
            html.Div(id='dimensions-rudder'),
            html.Br(),
            html.H5("Keel"),
            html.Div(id='dimensions-keel'),
            html.Br(),
            html.H5("Extra data"),
            dbc.Label("Crew mass [kg]"), html.Br(),
            dbc.Input(type='text', id='crewmass-min', bs_size="sm", value=format(round(200,2)), className='boxminimum'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='crewmass', bs_size="sm", value=format(round(280,2)), className='boxinput'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='crewmass-max', bs_size="sm", value=format(round(360,2)), className='boxmaximum'),
            
            dbc.Label("Ballast Ratio [%]"), html.Br(),
            dbc.Input(type='text', id='ballast-ratio-min', bs_size="sm", value=format(round(26,2)), className='boxminimum'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='ballast-ratio', bs_size="sm", value=format(round(28,2)), className='boxinput'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='ballast-ratio-max', bs_size="sm", value=format(round(58,2)), className='boxmaximum'),
            
            dbc.Label("Keel Naca Profile"),
            dcc.Dropdown(
                id='keel-naca',
                options=[
                    {"label": "4 digits", "value": '1'},
                    {"label": "6 digits", "value": '2'},
                ],
                value='1',
                style={'width': '100%', 'font-size': '10pt'},
            ),
            dbc.Label("Rudder Naca Profile"),
            dcc.Dropdown(
                id='rudder-naca',
                options=[
                    {"label": "4 digits", "value": '1'},
                    {"label": "6 digits", "value": '2'},
                ],
                value='1',
                style={'width': '100%', 'font-size': '10pt'},
            ),
            dbc.Label("Bulb keel"),
            dcc.Dropdown(
                id='bulbo-check',
                options=[
                    {"label": "Do not include", "value": '0'},
                    {"label": "Include", "value": '1'},
                ],
                value='0',
                style={'width': '100%', 'font-size': '10pt'},
            ),
            html.Div(id="dimensions-bulbo")
        ], width=3),
        dbc.Col([
            html.H5("Side plan view"),
            html.Div(dcc.Graph(id='plot-appendages', style={'width': 'inherit'})),
            html.Br(), html.Br(),
            html.Div(id="dimension-loa"),
        ], width=6),
    ]),
], className="mt-4",)


import dash
import numpy as np
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app
import plotly.graph_objs as go
import json, codecs
from scipy.integrate import simps
import pandas as pd


@app.callback(Output('dimensions-hull', 'children'),
    [Input('bwl-new', 'value')])
def create_sac(bwlnew):
    boa=np.float(bwlnew)*1.3
    return html.Div([
        dbc.Label("Free Board [m]"),
        dbc.Input(type='number', id='freeboard', bs_size="sm", value=1.5),
        dbc.Label("Bow angle [degrees]"),
        dbc.Input(type='number', id='bowangle', bs_size="sm", value=15),
        dbc.Label("Overhang [m]"),
        dbc.Input(type='number', id='overhang', bs_size="sm", value=1),
        dbc.Label("Maximum beam [m]"),
        dbc.Input(type='number', id='boa', bs_size="sm", value="{}".format(round(boa,2))),
    ])

@app.callback(Output('dimensions-new', 'children'),
    [Input('sailset', 'value')])
def create_sac(sailset):
    dimensions = pd.read_csv("data/initialhull.csv")
    lwl = min(dimensions["LWL"])
    bwl = min(dimensions["BWL"])
    tc=0.57
    disp=8
    lcb = 4.4
    lcf = 4.9
    return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Waterline length [m]"),
                    dbc.Input(type='text', id='lwl-new', bs_size="sm", value="{}".format(round(lwl,2))),
                    dbc.Label("Waterline beam [m]"),
                    dbc.Input(type='text', id='bwl-new', bs_size="sm", value="{}".format(round(bwl,2))),
                    dbc.Label("Draft [m]"),
                    dbc.Input(type='text', id='tc-new', bs_size="sm", value="{}".format(round(tc,2))),
                ]),
                dbc.Col([
                    dbc.Label("Displacement [m3]"),
                    dbc.Input(type='text', id='disp-new', bs_size="sm", value="{}".format(round(disp,2))),
                    dbc.Label("LCB [m]"),
                    dbc.Input(type='text', id='lcb-new', bs_size="sm", value="{}".format(round(lcb,2))),
                    dbc.Label("LCF [m]"),
                       dbc.Input(type='text', id='lcf-new', bs_size="sm", value="{}".format(round(lcf,2))),
                ]),
            ]),	
        ])

@app.callback(Output('plot-appendages', 'figure'),
    [Input('sailset', 'value'), Input('bowangle', 'value'), Input('freeboard', 'value'), Input('rootchord-rudder', 'value'), Input('tipchord-rudder', 'value'), Input('span-rudder', 'value'), Input('sweep-rudder', 'value'), Input('heightsurface-rudder', 'value'), Input('ce-rudder', 'value'), Input('rootchord-keel', 'value'), Input('tipchord-keel', 'value'), Input('span-keel', 'value'), Input('sweep-keel', 'value'), Input('ce-keel', 'value'), Input('overhang', 'value'), Input('boom-height', 'value'), Input('lcb-new', 'value'), Input('lcf-new', 'value'), Input('lwl-new', 'value'), Input('tc-new', 'value')])
def create_sac(sailset, bowangle, freeboard, rootrudder, tiprudder, spanrudder, sweeprudder, hsr, cerudder, rootkeel, tipkeel, spankeel, sweepkeel, cekeel, overhang, boomheight, lcbnew, lcfnew, lwlnew, tcnew):
    tc = -np.float(tcnew)
    lwl = np.float(lwlnew)
    lcbnew = np.float(lcbnew)
    lcfnew = np.float(lcfnew)

    sailset = np.float(sailset)
    bowangle = np.radians(np.float(bowangle))
    freeboard = np.float(freeboard)
    rootrudder = np.float(rootrudder)
    tiprudder = np.float(tiprudder)
    spanrudder = np.float(spanrudder)
    sweeprudder = np.radians(np.float(sweeprudder))
    cerudder = np.float(cerudder)
    rootkeel = np.float(rootkeel)
    tipkeel = np.float(tipkeel)
    spankeel = np.float(spankeel)
    sweepkeel = np.radians(np.float(sweepkeel))
    hsr = np.float(hsr)
    cekeel = np.float(cekeel)
    bow_x = (np.tan(bowangle)*freeboard)+lwl
    bow_y = freeboard
    boomheight = np.float(boomheight)
    overhangx = -np.float(overhang)
    overhangy = -overhangx/4
    lbk=1.3
    tbk=0.3
    p=15
    e=4.5
    j=7
    masttcks=0.2
    mastdeflection=0.15
    zcbk = -1
    xcbk = lwl/2
    return {
        'data': [
            go.Scatter(
                x=[xcbk],
                y=[zcbk],
                text=['CE keel'],
                name='Centre of Effort - Keel',
                cliponaxis=False,
            ),
            go.Scatter(
                x=[lcfnew],
                y=[-0.1],
                text=['LCF'],
                name='LCF',
                cliponaxis=False,
            ),
            go.Scatter(
                x=[lcbnew],
                y=[-0.1],
                text=['LCB'],
                name='LCB',
                cliponaxis=False,
            ),
        ],
        'layout': go.Layout(
            height=800,
            xaxis= {
                'range': [-1, bow_x*1.1],
                'zeroline': False,
                'title': "Length [m]",
                'dtick': 1, 
            },
            yaxis= {
                'range': [-3, p+freeboard+2],
                'showgrid': False,
                'title': "Height [m]",
                'scaleanchor':"x",
                'scaleratio': 1,
            },
            margin = {
                "r": 30,
                "t": 30,
                "b": 30,
                "l": 30
            },
            shapes= [
            {#mast
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(lwl/2, bow_y*1.1, lwl/2+masttcks, bow_y*1.1, lwl/2+masttcks-mastdeflection, freeboard+boomheight+p, lwl/2-mastdeflection, freeboard+boomheight+p),
                'layer': 'above',
                'fillcolor': 'white',
                'line': {'width': 1},
            },
            {#main sail
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} Z'.format(lwl/2-mastdeflection, freeboard+boomheight+p, lwl/2-e, freeboard+boomheight, lwl/2, freeboard+boomheight),
                'layer': 'below',
                'fillcolor': 'rgba(255, 140, 184, 0.1)',
                'line': {'width': 1},
            },
            {#main sail
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(lwl/2, freeboard+boomheight, lwl/2-e-0.25, freeboard+boomheight, lwl/2-e-0.25, freeboard+boomheight-0.25, lwl/2, freeboard+boomheight-0.25),
                'layer': 'above',
                'fillcolor': 'white',
                'line': {'width': 1},
            },
            {#jib sail
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} Z'.format(lwl/2+masttcks-mastdeflection, freeboard+boomheight+p, bow_x, bow_y, bow_x-j, freeboard+boomheight*0.5) if sailset == 1 or sailset == 3 else '',
                'layer': 'below',
                'fillcolor': 'rgba(93, 164, 214, 0.1)',
                'line': {'width': 1},
            },
            {#spinnaker sail
                'type': 'path',
                'path': 'M {},{} Q {},{} {},{}'.format(lwl*0.65, freeboard+p/8,lwl*0.85, freeboard+p*0.15, bow_x,bow_y) if sailset == 2 or sailset == 3 else '',
                'layer': 'below',
                'line': {'width': 1},
            },
            {#spinnaker sail
                'type': 'path',
                'path': 'M {},{} Q {},{} {},{}'.format(lwl*0.65, freeboard+p/8,lwl*0.8, freeboard+p/2, lwl/2,freeboard+p*0.9) if sailset == 2 or sailset == 3 else '',
                'layer': 'below',
                'line': {'width': 1},
            },
            {#spinnaker sail
                'type': 'path',
                'path': 'M {},{} Q {},{} {},{}'.format(lwl/2, freeboard+p*0.9,bow_x*1.1, freeboard+p*0.8, bow_x,bow_y) if sailset == 2 or sailset == 3 else '',
                'layer': 'below',
                'line': {'width': 1},
            },
            { #spinnaker
            'type': 'line',
                'x0': lwl*0.65 if sailset == 2 or sailset == 3 else '',
                'y0': freeboard+p/8 if sailset == 2 or sailset == 3 else '',
                'x1': 0 if sailset == 2 or sailset == 3 else '',
                'y1': 0 if sailset == 2 or sailset == 3 else '',
                'layer': 'below',
                'line': {'width': 1, 'color': 'grey'},
            },
            {#deck2
                'type': 'path',
                'path': ' M {},{} L {},{} L {},{} L {},{}'.format(lwl*0.33, bow_y*0.7, lwl*0.35, bow_y*1.2, lwl*0.58, bow_y*1.2, lwl*0.85, bow_y*0.6),
                'layer': 'above',
                'fillcolor': 'white',
                'line': {'width': 1},
            },
            {#deck1
                'type': 'path',
                'path': ' M 0,0 L{},{} L{},{} L{},{}, L{},{} L{},{} Z'.format(overhangx, overhangy, overhangx*0.9, bow_y*0.5, 0,bow_y*0.8,bow_x,bow_y, lwl,0),
                'layer': 'above',
                'fillcolor': 'white',
                'line': {'width': 1},
            },
            
            {#rudder
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(cerudder-rootrudder/2, hsr, cerudder+rootrudder/2, hsr, cerudder+rootrudder/2-np.tan(sweeprudder)*spanrudder, hsr-spanrudder, cerudder+rootrudder/2-np.tan(sweeprudder)*spanrudder-tiprudder, hsr-spanrudder),
                'layer': 'below',
                'line': {'width': 1},
            },
            {#keel
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(cekeel-rootkeel/2, 0, cekeel+rootkeel/2, 0, cekeel+rootkeel/2-np.tan(sweepkeel)*spankeel, tc-spankeel, cekeel+rootkeel/2-np.tan(sweepkeel)*spankeel-tipkeel, tc-spankeel),
                'layer': 'below',
                'line': {'width': 1},
            },
            { #keel curve
                'type': 'path',
                'path': 'M 0,0 C {},{} {},{} {},0'.format(lwl/4, tc*1.35, 3*lwl/4, tc*1.35, lwl),
                'line': {'color': 'black'},
                'fillcolor': 'white',
                'layer': 'below',
                'line': {'width': 1},
            },
            { #bow
            'type': 'line',
                'x0': lwl,
                'y0': 0,
                'x1': bow_x,
                'y1': bow_y,
                'line': {'width': 1},
            },
            { #waterline
            'type': 'line',
                'x0': -6,
                'y0': 0,
                'x1': 50,
                'y1': 0,
                'line': {'width': 1, 'color': 'rgb(78,179,211,0.05)'},
            },
            ],
            font=dict(size=10),
            legend=dict(x=0, y=1),
        )
    }

@app.callback(Output('dimension-loa', 'children'),
    [Input('overhang', 'value'), Input('bowangle', 'value'), Input('freeboard', 'value')])
def create_sac(overhang, bowangle, freeboard):
    lwl =10
    loa = np.float(lwl)+np.float(overhang)+np.tan(np.radians(np.float(bowangle)))*np.float(freeboard)
    loaft = loa/0.3048
    return html.Div(dbc.Row(dbc.Col(dbc.Label("The overall lenght of the vessel is {} feet, equivalent to {} meters.".format(np.round(loaft,0), np.round(loa,2)))))),
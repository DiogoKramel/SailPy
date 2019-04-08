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
    [Input('bwl-new', 'value'), Input('lwl-new', 'value'), Input('tc-new', 'value')])
def dimensionshull(bwlnew, lwlnew, tcnew):
    boa = np.float(bwlnew)*1.3
    freeboard = np.float(tcnew)*1.65
    overhang = np.float(lwlnew)/10
    return html.Div([
        dbc.Label("Free Board [m]"),
        dbc.Input(type='text', id='freeboard', bs_size="sm", value=format(round(freeboard,2))),
        dbc.Label("Maximum beam [m]"),
        dbc.Input(type='text', id='boa', bs_size="sm", value=format(round(boa,2))),
        dbc.Label("Overhang [m]"),
        dbc.Input(type='text', id='overhang', bs_size="sm", value=format(round(overhang,2))),
        dbc.Label("Bow angle [deg]"),
        dbc.Input(type='text', id='bowangle', bs_size="sm", value=15),
    ])

@app.callback(Output('dimensions-sail', 'children'),
    [Input('sailset', 'value'), Input('disp-new', 'value'), Input('lwl-new', 'value')])
def dimensionssail(sailset, disp, lwl):
    lwl = np.float(lwl)
    ar = 2.95
    sa = 18*np.float(disp)**(2/3)
    sm = sa*0.6
    p = (2*sm*ar)**0.5
    e=2*sm/p
    i=p*0.9
    j=2*(sa-sm)/i
    lpg = 1.5*j
    spl = 1.1*p
    mastheight = 1.2+np.float(p)+0.2
    mastpos = lwl*0.6
    return html.Div([
        dbc.Label("Mainsail hoist - P [m]"),
        dbc.Input(type='text', id='psail', bs_size="sm", value=round(p,2)),
        dbc.Label("Mainsail foot - E [m]"),
        dbc.Input(type='text', id='esail', bs_size="sm", value=round(e,2)),
        dbc.Label("Jib height - I [m]"),
        dbc.Input(type='text', id='isail', bs_size="sm", value=round(i,2)),
        dbc.Label("Jib base - J [m]"),
        dbc.Input(type='text', id='jsail', bs_size="sm", value=round(j,2)),
        dbc.Label("Perpendicular of longest jib [m]"),
        dbc.Input(type='text', id='lpg', bs_size="sm", value=round(lpg,2)),
        dbc.Label("Spinnaker leech length [m]"),
        dbc.Input(type='text', id='spl', bs_size="sm", value=round(spl,2)),
        dbc.Label("Mast average diameter [m]"),
        dbc.Input(type='text', id='mast-diameter', bs_size="sm", value=0.2),
        dbc.Label("Height of main boom above sheer [m]"),
        dbc.Input(type='text', id='boom-height', bs_size="sm", value=1.2),
        dbc.Label("Mast height above sheerline [m]"),
        dbc.Input(type='text', id='mast-height', bs_size="sm", value=round(mastheight,2)),
        dbc.Label("Mast longitudinal position [m]"),
        dbc.Input(type='text', id='mastpos', bs_size="sm", value=round(mastpos,2)),
    ])

@app.callback(Output('dimensions-mast', 'children'),
    [Input('boom-height', 'value'), Input('psail', 'value')])
def dimensionsmast(boomheight, psail):
    mastheight = np.float(boomheight)+np.float(psail)+0.2
    return html.Div([
        dbc.Label("Mast height above sheerline [m]"),
        dbc.Input(type='text', id='mast-height', bs_size="sm", value=round(mastheight,2)),
    ])

@app.callback(Output('dimensions-rudder', 'children'),
    [Input('lwl-new', 'value'), Input('disp-new', 'value')])
def dimensionsrudder(lwl, disp):
    lwl = np.float(lwl)
    t =lwl/(0.19*lwl+4.0533)
    spanrudder = t*0.8
    sa = 18*np.float(disp)**(2/3)
    surfacerudder = 0.01*sa
    tiprudder=0.7*surfacerudder/spanrudder
    rootrudder=1.1*surfacerudder/spanrudder
    return html.Div([
        dbc.Label("Root Chord"),
        dbc.Input(type='text', id='rootchord-rudder', bs_size="sm", value=round(rootrudder,2)),
        dbc.Label("Tip chord"),
        dbc.Input(type='text', id='tipchord-rudder', bs_size="sm", value=round(tiprudder,2)),
        dbc.Label("Span"),
        dbc.Input(type='text', id='span-rudder', bs_size="sm", value=round(spanrudder,2)),
        dbc.Label("Sweep angle [degrees]"),
        dbc.Input(type='text', id='sweep-rudder', bs_size="sm", value=15),
        dbc.Label("Height above or below waterline"),
        dbc.Input(type='text', id='heightsurface-rudder', bs_size="sm", value=-0.05),
        dbc.Label("Root Centerline"),
        dbc.Input(type='text', id='pos-rudder', bs_size="sm", value=1),
        dbc.Label("Root Chord Thickness"),
        dbc.Input(type='text', id='rootchord-rudder-tcks', bs_size="sm", value=0.175),
        dbc.Label("Tip Chord Thickness"),
        dbc.Input(type='text', id='tipchord-rudder-tcks', bs_size="sm", value=0.105),
    ])

@app.callback(Output('dimensions-keel', 'children'),
    [Input('lwl-new', 'value'), Input('tc-new', 'value'), Input('disp-new', 'value')])
def dimensionskeel(lwl, tc, disp):
    lwl = np.float(lwl)
    cekeel = lwl/2
    lwl = np.float(lwl)
    t =lwl/(0.19*lwl+4.0533)
    spankeel = t*np.float(tc)
    sa = 18*np.float(disp)**(2/3)
    surfacekeel = 0.03*sa
    tipkeel=0.8*surfacekeel/spankeel
    rootkeel=1.2*surfacekeel/spankeel
    return html.Div([
        dbc.Label("Root Chord"),
        dbc.Input(type='text', id='rootchord-keel', bs_size="sm", value=round(rootkeel,2)),
        dbc.Label("Tip Chord"),
        dbc.Input(type='text', id='tipchord-keel', bs_size="sm", value=round(tipkeel,2)),
        dbc.Label("Span"),
        dbc.Input(type='text', id='span-keel', bs_size="sm", value=round(spankeel,2)),
        dbc.Label("Sweep angle [degrees]"),
        dbc.Input(type='text', id='sweep-keel', bs_size="sm", value=20),
        dbc.Label("Root Centerline"),
        dbc.Input(type='text', id='pos-keel', bs_size="sm", value=round(cekeel,2)),
        dbc.Label("Root Chord Thickness"),
        dbc.Input(type='text', id='rootchord-keel-tcks', bs_size="sm", value=0.175),
        dbc.Label("Tip Chord Thickness"),
        dbc.Input(type='text', id='tipchord-keel-tcks', bs_size="sm", value=0.105),
    ])

@app.callback(Output('dimensions-mizzen', 'children'),
    [Input('mzn-check', 'value')])
def dimensionskeel(mzncheck):
    if mzncheck == '0':
        return html.Div([
            dbc.Label("Mizzen Hoist"),
            dbc.Input(type='text', id='pmz', bs_size="sm", value=0),
            dbc.Label("Mizzen Foot"),
            dbc.Input(type='text', id='emz', bs_size="sm", value=0),
            dbc.Label("Boom height"),
            dbc.Input(type='text', id='badmz', bs_size="sm", value=0)
        ])
    if mzncheck == '1':
        return html.Div([
            dbc.Label("Mizzen Hoist"),
            dbc.Input(type='text', id='pmz', bs_size="sm", value=5),
            dbc.Label("Mizzen Foot"),
            dbc.Input(type='text', id='emz', bs_size="sm", value=3),
            dbc.Label("Boom height"),
            dbc.Input(type='text', id='badmz', bs_size="sm", value=1)
        ])

@app.callback(Output('dimensions-bulbo', 'children'),
    [Input('bulbo-check', 'value')])
def dimensionskeel(bulbocheck):
    if bulbocheck == '0':
        return html.Div([html.P("")])
    if bulbocheck == '1':
        return html.Div([
            dbc.Label("Keel bulbous length"),
            dbc.Input(type='text', id='lbk', bs_size="sm", value=0),
            dbc.Label("Keel bulbous lateral area"),
            dbc.Input(type='text', id='abk', bs_size="sm", value=0),
            dbc.Label("Keel bulbous wetted area"),
            dbc.Input(type='text', id='sbk', bs_size="sm", value=0)
        ])

@app.callback(Output('dimension-loa', 'children'),
    [Input('overhang', 'value'), Input('boa', 'value'), Input('bowangle', 'value'), Input('freeboard', 'value')])#, Input('jsail', 'value'), Input('lpg', 'value'), Input('spl', 'value'), Input('mast-diameter', 'value'), Input('boom-height', 'value'), Input('mast-height', 'value'), Input('rootchord-keel', 'value'), Input('tipchord-keel', 'value'), Input('span-keel', 'value'), Input('sweep-keel', 'value'), Input('pos-keel', 'value'), Input('rootchord-rudder', 'value'), Input('tipchord-rudder', 'value'), Input('span-rudder', 'value'), Input('sweep-rudder', 'value'), Input('pos-rudder', 'value'), Input('heightsurface-rudder', 'value')])
def dimensionloa(overhang, boa, bowangle, freeboard):
    lwl =10
    loa = np.float(lwl)+np.float(overhang)+np.tan(np.radians(np.float(bowangle)))*np.float(freeboard)
    loaft = loa/0.3048
    return html.Div(dbc.Row(dbc.Col(dbc.Label("The overall lenght of the vessel is {} feet, equivalent to {} meters.".format(np.round(loaft,0), np.round(loa,2)))))),
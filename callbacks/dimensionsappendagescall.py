import dash
import numpy as np
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from app import app
import plotly.graph_objs as go
import json, codecs
from scipy.integrate import simps
import pandas as pd


@app.callback(Output('dimension-boa', 'children'), [Input('bwl-new', 'value')])
def dimensionshull(bwlnew):
    boa = np.float(bwlnew)*1.3
    return html.Div([
        dbc.Label("Maximum beam [m]"), html.Br(),
        dbc.Input(type='text', id='boa-min', bs_size="sm", value=format(round(boa*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='boa', bs_size="sm", value=format(round(boa,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='boa-max', bs_size="sm", value=format(round(boa*1.1,2)), className='boxmaximum'),
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
        dbc.Label("Mainsail hoist - P [m]"), html.Br(),
        dbc.Input(type='text', id='psail-min', bs_size="sm", value=format(round(p*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='psail', bs_size="sm", value=format(round(p,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='psail-max', bs_size="sm", value=format(round(p*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Mainsail foot - E [m]"), html.Br(),
        dbc.Input(type='text', id='esail-min', bs_size="sm", value=format(round(e*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='esail', bs_size="sm", value=format(round(e,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='esail-max', bs_size="sm", value=format(round(e*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Jib height - I [m]"), html.Br(),
        dbc.Input(type='text', id='isail-min', bs_size="sm", value=format(round(i*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='isail', bs_size="sm", value=format(round(i,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='isail-max', bs_size="sm", value=format(round(i*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Jib base - J [m]"), html.Br(),
        dbc.Input(type='text', id='jsail-min', bs_size="sm", value=format(round(j*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='jsail', bs_size="sm", value=format(round(j,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='jsail-max', bs_size="sm", value=format(round(j*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Perpendicular of longest jib [m]"), html.Br(),
        dbc.Input(type='text', id='lpg-min', bs_size="sm", value=format(round(lpg*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='lpg', bs_size="sm", value=format(round(lpg,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='lpg-max', bs_size="sm", value=format(round(lpg*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Spinnaker leech length [m]"), html.Br(),
        dbc.Input(type='text', id='spl-min', bs_size="sm", value=format(round(spl*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='spl', bs_size="sm", value=format(round(spl,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='spl-max', bs_size="sm", value=format(round(spl*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Mast average diameter [m]"), html.Br(),
        dbc.Input(type='text', id='mast-diameter-min', bs_size="sm", value=format(round(0.2*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='mast-diameter', bs_size="sm", value=format(round(0.2,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='mast-diameter-max', bs_size="sm", value=format(round(0.2*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Height of main boom above sheer [m]"), html.Br(),
        dbc.Input(type='text', id='boom-height-min', bs_size="sm", value=format(round(1.2*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='boom-height', bs_size="sm", value=format(round(1.2,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='boom-height-max', bs_size="sm", value=format(round(1.2*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Mast height above sheerline [m]"), html.Br(),
        dbc.Input(type='text', id='mast-height-min', bs_size="sm", value=format(round(mastheight*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='mast-height', bs_size="sm", value=format(round(mastheight,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='mast-height-max', bs_size="sm", value=format(round(mastheight*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Mast longitudinal position [m]"), html.Br(),
        dbc.Input(type='text', id='mastpos-min', bs_size="sm", value=format(round(mastpos*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='mastpos', bs_size="sm", value=format(round(mastpos,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='mastpos-max', bs_size="sm", value=format(round(mastpos*1.1,2)), className='boxmaximum'),
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
        dbc.Label("Root Chord"), html.Br(),
        dbc.Input(type='text', id='rootchord-rudder-min', bs_size="sm", value=format(round(rootrudder*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='rootchord-rudder', bs_size="sm", value=format(round(rootrudder,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='rootchord-rudder-max', bs_size="sm", value=format(round(rootrudder*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Tip chord"), html.Br(),
        dbc.Input(type='text', id='tipchord-rudder-min', bs_size="sm", value=format(round(tiprudder*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='tipchord-rudder', bs_size="sm", value=format(round(tiprudder,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='tipchord-rudder-max', bs_size="sm", value=format(round(tiprudder*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Span"), html.Br(),
        dbc.Input(type='text', id='span-rudder-min', bs_size="sm", value=format(round(spanrudder*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='span-rudder', bs_size="sm", value=format(round(spanrudder,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='span-rudder-max', bs_size="sm", value=format(round(spanrudder*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Sweep angle [degrees]"), html.Br(),
        dbc.Input(type='text', id='sweep-rudder-min', bs_size="sm", value=format(round(0*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='sweep-rudder', bs_size="sm", value=format(round(15,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='sweep-rudder-max', bs_size="sm", value=format(round(30,2)), className='boxmaximum'),
        
        dbc.Label("Height above or below waterline"), html.Br(),
        dbc.Input(type='text', id='heightsurface-rudder-min', bs_size="sm", value=format(round(-0.1,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='heightsurface-rudder', bs_size="sm", value=format(round(-0.05,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='heightsurface-rudder-max', bs_size="sm", value=format(round(0,2)), className='boxmaximum'),
        
        dbc.Label("Root Centerline"), html.Br(),
        dbc.Input(type='text', id='pos-rudder-min', bs_size="sm", value=format(round(0*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='pos-rudder', bs_size="sm", value=format(round(1,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='pos-rudder-max', bs_size="sm", value=format(round(1.5*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Root Chord Thickness"), html.Br(),
        dbc.Input(type='text', id='rootchord-rudder-tcks-min', bs_size="sm", value=format(round(0.15*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='rootchord-rudder-tcks', bs_size="sm", value=format(round(0.175,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='rootchord-rudder-tcks-max', bs_size="sm", value=format(round(0.2*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Tip Chord Thickness"), html.Br(),
        dbc.Input(type='text', id='tipchord-rudder-tcks-min', bs_size="sm", value=format(round(0.075*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='tipchord-rudder-tcks', bs_size="sm", value=format(round(0.105,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='tipchord-rudder-tcks-max', bs_size="sm", value=format(round(0.135*1.1,2)), className='boxmaximum'),
        dbc.Input(type='text', id='tipchord-rudder-tcks', bs_size="sm", value=0.105),
    ])

@app.callback(Output('dimensions-keel', 'children'),
    [Input('lwl-new', 'value'), Input('tc-new', 'value'), Input('disp-new', 'value')])
def dimensionskeel(lwl, tc, disp):
    lwl = np.float(lwl)
    cekeel = lwl/2
    lwl = np.float(lwl)
    t =lwl/(0.19*lwl+4.0533)
    spankeel = t-np.float(tc)
    sa = 18*np.float(disp)**(2/3)
    surfacekeel = 0.03*sa
    tipkeel=0.8*surfacekeel/spankeel
    rootkeel=1.2*surfacekeel/spankeel
    return html.Div([
        dbc.Label("Root Chord"), html.Br(),
        dbc.Input(type='text', id='rootchord-keel-min', bs_size="sm", value=format(round(rootkeel*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='rootchord-keel', bs_size="sm", value=format(round(rootkeel,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='rootchord-keel-max', bs_size="sm", value=format(round(rootkeel*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Tip Chord"), html.Br(),
        dbc.Input(type='text', id='tipchord-keel-min', bs_size="sm", value=format(round(tipkeel*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='tipchord-keel', bs_size="sm", value=format(round(tipkeel,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='tipchord-keel-max', bs_size="sm", value=format(round(tipkeel*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Span"), html.Br(),
        dbc.Input(type='text', id='span-keel-min', bs_size="sm", value=format(round(spankeel*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='span-keel', bs_size="sm", value=format(round(spankeel,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='span-keel-max', bs_size="sm", value=format(round(spankeel*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Sweep angle [degrees]"), html.Br(),
        dbc.Input(type='text', id='sweep-keel-min', bs_size="sm", value=format(round(20*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='sweep-keel', bs_size="sm", value=format(round(35,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='sweep-keel-max', bs_size="sm", value=format(round(50*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Root Centerline"), html.Br(),
        dbc.Input(type='text', id='pos-keel-min', bs_size="sm", value=format(round(cekeel*0.9,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='pos-keel', bs_size="sm", value=format(round(cekeel,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='pos-keel-max', bs_size="sm", value=format(round(cekeel*1.1,2)), className='boxmaximum'),
        
        dbc.Label("Root Chord Thickness"), html.Br(),
        dbc.Input(type='text', id='rootchord-keel-tcks-min', bs_size="sm", value=format(round(0.15,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='rootchord-keel-tcks', bs_size="sm", value=format(round(0.175,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='rootchord-keel-tcks-max', bs_size="sm", value=format(round(0.2,2)), className='boxmaximum'),
        
        dbc.Label("Tip Chord Thickness"), html.Br(),
        dbc.Input(type='text', id='tipchord-keel-tcks-min', bs_size="sm", value=format(round(0.07,2)), className='boxminimum'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='tipchord-keel-tcks', bs_size="sm", value=format(round(0.1,2)), className='boxinput'),
        html.P(" ", className='spacebox'),
        dbc.Input(type='text', id='tipchord-keel-tcks-max', bs_size="sm", value=format(round(0.13,2)), className='boxmaximum'),
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
            dbc.Label("Mizzen Hoist"), html.Br(),
            dbc.Input(type='text', id='pmz-min', bs_size="sm", value=format(round(3,2)), className='boxminimum'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='pmz', bs_size="sm", value=format(round(4,2)), className='boxinput'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='pmz-max', bs_size="sm", value=format(round(5,2)), className='boxmaximum'),
            
            dbc.Label("Mizzen Foot"), html.Br(),
            dbc.Input(type='text', id='emz-min', bs_size="sm", value=format(round(1,2)), className='boxminimum'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='emz', bs_size="sm", value=format(round(2,2)), className='boxinput'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='emz-max', bs_size="sm", value=format(round(3,2)), className='boxmaximum'),
            
            dbc.Label("Boom height"), html.Br(),
            dbc.Input(type='text', id='badmz-min', bs_size="sm", value=format(round(0.7,2)), className='boxminimum'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='badmz', bs_size="sm", value=format(round(1,2)), className='boxinput'),
            html.P(" ", className='spacebox'),
            dbc.Input(type='text', id='badmz-max', bs_size="sm", value=format(round(1.3,2)), className='boxmaximum'),
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

@app.callback(Output('dimension-loa', 'children'), [Input('lwl-new', 'value'), Input('overhang', 'value'), Input('bowangle', 'value'), Input('freeboard', 'value'), Input('disp-new', 'value'), Input('ballast-ratio', 'value'), Input('tc-new', 'value'), Input('bwl-new', 'value')])
def dimensionloa(lwl, overhang, bowangle, freeboard, disp, br, tc, bwl):
    loa = np.float(lwl)+np.float(overhang)+np.tan(np.radians(np.float(bowangle)))*np.float(freeboard)
    loaft = loa/0.3048
    boa = np.float(bwl)*1.1
    dispmass = np.float(disp)*1025
    br = np.float(br)/100
    ssv = boa**2/(br*np.float(tc)*np.float(disp)**(1/3))
    print(ssv)       
    avs = 110+(400/(ssv-10))
    print(avs)
    cs = boa*3.28084/(dispmass*2.20462/64)**(1/3)
    cr = np.float(disp)*1025*2.20462/((boa*3.28084)**(4/3)*0.65*(0.7*np.float(lwl)*3.28084+0.3*loa*3.28084))

    data = {'Parameters' : ['Angle of Vanishing Stability', 'Capsize Screening Factor', 'Comfort Ratio'], 'Values' : [round(avs,2), round(cs,2), round(cr,2)], 'Recommendation' : ['> 110', '< 2', '> 30'], 'Unit' : ['degrees', '-', '-']}
    df = pd.DataFrame(data)

    return html.Div([
        dbc.Row(
            dbc.Col([
                dbc.Label("The overall lenght of the vessel is {} feet, equivalent to {} meters.".format(np.round(loaft,0), np.round(loa,2))),
                html.Br(), html.Br(),
                dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict("rows"),
                    style_cell={'textAlign': 'center', 'minWidth': '0px', 'maxWidth': '150px', 'whiteSpace': 'normal'},
                    style_cell_conditional=[{'if': {'column_id': 'Parameters'}, 'textAlign': 'left'}],
                    style_as_list_view=True,
                    style_header={'fontWeight': 'bold'},
                )
            ]),
        ),
    ]),
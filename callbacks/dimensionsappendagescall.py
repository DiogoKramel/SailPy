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

from functions import vpp_solve


@app.callback(Output('dimension-boa', 'children'), [Input('bwl-new', 'value')])
def dimensionshull(bwlnew):
    boa = np.float(bwlnew)*1.3
    return html.Div([
        dbc.Label("Beam [m]"), html.Br(),
        dbc.Input(type='text', id='boa', bs_size="sm", value=format(round(boa,2)), className='boxinput'),
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
    if sailset == "1" or sailset == "3":
        i=p*0.9
        j=2*(sa-sm)/i
    elif sailset == "2" or sailset == "4":
        i=0
        j=0
    lpg = 1.5*j
    spl = 1.1*p
    mastheight = 1.2+np.float(p)+0.2
    mastpos = lwl*0.6
    return html.Div([
        dbc.Label("Mainsail hoist - P [m]"), html.Br(),
        dbc.Input(type='text', id='psail', bs_size="sm", value=format(round(p,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Mainsail foot - E [m]"), html.Br(),
        dbc.Input(type='text', id='esail', bs_size="sm", value=format(round(e,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Jib height - I [m]"), html.Br(),
        dbc.Input(type='text', id='isail', bs_size="sm", value=format(round(i,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Jib base - J [m]"), html.Br(),
        dbc.Input(type='text', id='jsail', bs_size="sm", value=format(round(j,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Perpendicular of longest jib [m]"), html.Br(),
        dbc.Input(type='text', id='lpg', bs_size="sm", value=format(round(lpg,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Spinnaker leech length [m]"), html.Br(),
        dbc.Input(type='text', id='spl', bs_size="sm", value=format(round(spl,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Mast average diameter [m]"), html.Br(),
        dbc.Input(type='text', id='mast-diameter', bs_size="sm", value=format(round(0.2,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Height of main boom above sheer [m]"), html.Br(),
        dbc.Input(type='text', id='boom-height', bs_size="sm", value=format(round(1.2,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Mast height above sheerline [m]"), html.Br(),
        dbc.Input(type='text', id='mast-height', bs_size="sm", value=format(round(mastheight,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Mast longitudinal position [m]"), html.Br(),
        dbc.Input(type='text', id='mastpos', bs_size="sm", value=format(round(mastpos,2)), className='boxinput'), html.Br(),
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
        dbc.Input(type='text', id='rootchord-rudder', bs_size="sm", value=format(round(rootrudder,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Tip chord"), html.Br(),
        dbc.Input(type='text', id='tipchord-rudder', bs_size="sm", value=format(round(tiprudder,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Span"), html.Br(),
        dbc.Input(type='text', id='span-rudder', bs_size="sm", value=format(round(spanrudder,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Sweep angle [degrees]"), html.Br(),
        dbc.Input(type='text', id='sweep-rudder', bs_size="sm", value=format(round(15,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Height above or below waterline"), html.Br(),
        dbc.Input(type='text', id='heightsurface-rudder', bs_size="sm", value=format(round(-0.05,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Root Centerline"), html.Br(),
        dbc.Input(type='text', id='pos-rudder', bs_size="sm", value=format(round(1,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Root Chord Thickness"), html.Br(),
        dbc.Input(type='text', id='rootchord-rudder-tcks', bs_size="sm", value=format(round(0.175,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Tip Chord Thickness"), html.Br(),
        dbc.Input(type='text', id='tipchord-rudder-tcks', bs_size="sm", value=format(round(0.105,2)), className='boxinput'), html.Br(),
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
        dbc.Input(type='text', id='rootchord-keel', bs_size="sm", value=format(round(rootkeel,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Tip Chord"), html.Br(),
        dbc.Input(type='text', id='tipchord-keel', bs_size="sm", value=format(round(tipkeel,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Span"), html.Br(),
        dbc.Input(type='text', id='span-keel', bs_size="sm", value=format(round(spankeel,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Sweep angle [degrees]"), html.Br(),
        dbc.Input(type='text', id='sweep-keel', bs_size="sm", value=format(round(35,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Root Centerline"), html.Br(),
        dbc.Input(type='text', id='pos-keel', bs_size="sm", value=format(round(cekeel,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Root Chord Thickness"), html.Br(),
        dbc.Input(type='text', id='rootchord-keel-tcks', bs_size="sm", value=format(round(0.175,2)), className='boxinput'), html.Br(),
        
        dbc.Label("Tip Chord Thickness"), html.Br(),
        dbc.Input(type='text', id='tipchord-keel-tcks', bs_size="sm", value=format(round(0.1,2)), className='boxinput'), html.Br(),
    ])

@app.callback(Output('dimensions-mizzen', 'children'),
    [Input('mzn-check', 'value')])
def mzncheck(mzncheck):
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
            dbc.Input(type='text', id='pmz', bs_size="sm", value=format(round(4,2)), className='boxinput'), html.Br(),
            
            dbc.Label("Mizzen Foot"), html.Br(),
            dbc.Input(type='text', id='emz', bs_size="sm", value=format(round(2,2)), className='boxinput'), html.Br(),
            
            dbc.Label("Boom height"), html.Br(),
            dbc.Input(type='text', id='badmz', bs_size="sm", value=format(round(1,2)), className='boxinput'), html.Br(),
        ])

@app.callback(Output('dimensions-bulbo', 'children'),
    [Input('bulbo-check', 'value')])
def bulbocheck(bulbocheck):
    if bulbocheck == '0':
        return html.Div([
            dbc.Label("Keel bulbous length"),
            dbc.Input(type='text', id='lbk', bs_size="sm", value=0),
            dbc.Label("Keel bulbous lateral area"),
            dbc.Input(type='text', id='abk', bs_size="sm", value=0),
            dbc.Label("Keel bulbous wetted area"),
            dbc.Input(type='text', id='sbk', bs_size="sm", value=0)
        ])
    if bulbocheck == '1':
        return html.Div([
            dbc.Label("Keel bulbous length"), html.Br(),
            dbc.Input(type='text', id='lbk', bs_size="sm", value=format(round(1,2)), className='boxinput'), html.Br(),
            
            dbc.Label("Keel bulbous lateral area"), html.Br(),
            dbc.Input(type='text', id='abk', bs_size="sm", value=format(round(1,2)), className='boxinput'), html.Br(),
            
            dbc.Label("Keel bulbous wetted area"), html.Br(),
            dbc.Input(type='text', id='sbk', bs_size="sm", value=format(round(1,2)), className='boxinput'), html.Br(),
        ])

@app.callback(Output('dimension-loa', 'children'), [Input('lwl-new', 'value'), Input('overhang', 'value'), Input('bowangle', 'value'), Input('freeboard', 'value'), Input('disp-new', 'value'), Input('ballast-ratio', 'value'), Input('tc-new', 'value'), Input('bwl-new', 'value')])
def dimensionloa(lwl, overhang, bowangle, freeboard, disp, br, tc, bwl):
    loa = np.float(lwl)+np.float(overhang)+np.tan(np.radians(np.float(bowangle)))*np.float(freeboard)
    loaft = loa/0.3048
    boa = np.float(bwl)*1.1
    dispmass = np.float(disp)*1025
    br = np.float(br)/100
    ssv = boa**2/(br*np.float(tc)*np.float(disp)**(1/3))
    avs = 110+(400/(ssv-10))
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
                    style_cell={'textAlign': 'center', 'minWidth': '0px', 'maxWidth': '150px', 'whiteSpace': 'normal', 'font_family': 'Source Sans Pro', 'font-size': '10pt',},
                    style_cell_conditional=[{'if': {'column_id': 'Parameters'}, 'textAlign': 'left'}],
                    style_as_list_view=True,
                    style_header={'fontWeight': 'bold'},
                )
            ]),
        ),
    ]),

@app.callback(Output('dimension-area', 'children'), [Input('rootchord-rudder', 'value'), Input('tipchord-rudder', 'value'), Input('span-rudder', 'value'), Input('rootchord-keel', 'value'), Input('tipchord-keel', 'value'), Input('span-keel', 'value'), Input('psail', 'value'), Input('esail', 'value'), Input('isail', 'value'), Input('jsail', 'value')])
def dimensionloa(rootrudder, tiprudder, spanrudder, rootkeel, tipkeel, spankeel, psail, esail, isail, jsail):
    arearudder = np.float(spanrudder)*(np.float(rootrudder)+np.float(tiprudder))/2
    areakeel = np.float(spankeel)*(np.float(rootkeel)+np.float(tipkeel))/2
    areasail = np.float(psail)*np.float(esail)/2+np.float(isail)*np.float(jsail)/2

    data = {'Dimensions' : ['Rudder Area', 'Keel Area', 'Sail Area'], 'Values' : [round(arearudder,2), round(areakeel,2), round(areasail,2)], 'Unit' : ['m2', 'm2', 'm2']}
    df = pd.DataFrame(data)

    return html.Div([
        dbc.Row(
            dbc.Col([
                dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in df.columns],
                    data=df.to_dict("rows"),
                    style_cell={'textAlign': 'center', 'minWidth': '0px', 'maxWidth': '90px', 'whiteSpace': 'normal', 'font_family': 'Source Sans Pro', 'font-size': '10pt',},
                    style_cell_conditional=[{'if': {'column_id': 'Dimensions'}, 'textAlign': 'left'}],
                    style_as_list_view=True,
                    style_header={'fontWeight': 'bold'},
                )
            ]),
        ),
    ]),

@app.callback(Output('polar-diagram2', 'figure'), [Input('lwl-new', 'value'), Input('bwl-new', 'value')])
def callback_vpp(lwl, bwl):

    velocity = [6, 8, 10]
    true_wind = [30, 60, 90, 120, 150, 180]
    # velocities = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    resultados = vpp_solve('main+genoa', np.float(lwl)*1.1, np.float(lwl), np.float(bwl)*1.1, np.float(bwl), 0.57, 0, 0, 0.35, 0.5, 0.7, 0.79, 4.5, 0.8, 1, 5.674, 1, \
            280, 16, 4, 14, 4, 1, 17, \
            33, 1.34, 0.38, 0.6, 0.1, 0.17, \
            15, 1.11, 1.58, 2.37, 0.1, 0.17, 0.6, \
            '6digit', '6digit', 17, 0.05, 0, 0, 0, 0, 0, 0, 0, \
            velocity[0], velocity[2]+1, true_wind[0], true_wind[5]+1)
    velocities = resultados[2]
    print(velocities)
            
    angles = true_wind

    return {
        'data': [go.Scatterpolar(
            theta=angles,
            r=velocity[0],
            mode='lines',
            name='6 knots'
        ),
        go.Scatterpolar(
            theta=angles,
            r=velocity[1],
            mode='lines',
            name='8 knots'
        ), 
        go.Scatterpolar(
            theta=angles,
            r=velocity[2],
            mode='lines',
            name='10 knots'
        )],
        # https://plot.ly/python/polar-chart/
        'layout': go.Layout(
            title='Velocity Prediction',
            hovermode = "closest",
            height = 500,
            margin = {
                "r": 20,
                "t": 30,
                "b": 50,
                "l": 50
            },
            polar = dict(
                sector = [0, 360],
                radialaxis = dict(
                    angle = 90,
                    range = [0, 6],
                ),
                angularaxis = dict(
                    direction = "clockwise",
                    rotation = 90,
                ),
            ),
            font=dict(size=10),
            legend=dict(x=0.3, y=-0.5),
        ),
    }
import dash
import numpy as np
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app
import plotly.graph_objs as go
import json
import codecs
from scipy.integrate import simps
import csv
import pandas as pd
import time

from functions import resistance
from functions import optimize_nsgaII


@app.callback(
    Output('resistance-weight', 'children'),
    [Input('weight1', 'value')])
def resistance_weight(value):
    return dbc.Label(': {}'.format(value))

@app.callback(
    Output('comfort-weight', 'children'),
    [Input('weight2', 'value')])
def comfort_weight(value):
    return dbc.Label(': {}'.format(value))

@app.callback(
    Output('dimensions-limits', 'children'),
    [Input('weight2', 'value')])
def comfort_weight(value):
    dimensionsobj = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
    dimensions = json.loads(dimensionsobj)
    for item in dimensions:
        item = str(item)
        if item != "category":
            globals()[item] = np.float(dimensions[item])
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Label("Waterline length"), html.Br(),
                dbc.Input(value="{}".format(round(lwl*0.9,2)), id='lwl-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(lwl,2)), style={'display': 'inline-block', 'padding': '5px'}),
                dbc.Input(value="{}".format(round(lwl*1.1,2)), id='lwl-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),

                html.Br(), dbc.Label("Waterline beam"), html.Br(),
                dbc.Input(value="{}".format(round(lwl/5,2)), id='bwl-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(bwl,2)), style={'display': 'inline-block', 'padding': '5px'}),
                dbc.Input(value="{}".format(round(lwl/2.73,2)), id='bwl-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),

                html.Br(), dbc.Label("Draft"), html.Br(),
                dbc.Input(value="{}".format(round(bwl/15,2)), type='text', id='tc-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(tc,2)), style={'display': 'inline-block', 'padding': '5px'}),
                dbc.Input(value="{}".format(round(bwl/2.46,2)), type='text', id='tc-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
            ]),
            dbc.Col([
                dbc.Row(dbc.Label("LCB")),
                dbc.Row([
                    dbc.Input(value="{}".format(round(lwl*0.418,2)), type='text', id='lcb-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                    html.P("{}m".format(round(lcb,2)), style={'display': 'inline-block', 'padding': '5px'}),
                    dbc.Input(value="{}".format(round(lwl*0.5,2)), type='text', id='lcb-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ]),
                dbc.Row(dbc.Label("LCF")),
                dbc.Row([
                    dbc.Input(value="{}".format(round(lwl*0.405,2)), type='text', id='lcf-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                    html.P("{}m".format(round(lcf,2)), style={'display': 'inline-block', 'padding': '5px'}),
                    dbc.Input(value="{}".format(round(lwl*0.482,2)), type='text', id='lcf-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ])
            ])
        ])
    ])

@app.callback(Output('output-button', 'children'), [Input('export-ga', 'n_clicks')], [State('pop-size', 'value'), State('children-size', 'value'), State('max-generation', 'value'), State('mut-prob', 'value'), State('halloffame-number', 'value'), State('indpb-value', 'value'), State('eta_value', 'value'), State('weight1', 'value'), State('weight2', 'value'), State('velocity-range', 'value'), State('heel-range', 'value'), State('lwl-min', 'value'), State('lwl-max', 'value'), State('bwl-min', 'value'), State('bwl-max', 'value'), State('tc-min', 'value'), State('tc-max', 'value'), State('lcb-min', 'value'), State('lcb-max', 'value'), State('lcf-min', 'value'), State('lcf-max', 'value'), State('ga-method', 'value')])
def update_output(n_clicks, popsize, childrensize, maxgeneration, mutprob, halloffamenumber, indpb, eta, weight1, weight2, velocityrange, heelrange, lwlmin, lwlmax, bwlmin, bwlmax, tcmin, tcmax, lcbmin, lcbmax, lcfmin, lcfmax, gamethod):
    if n_clicks == 1:
        json.dump({'popsize': popsize, 'childrensize': childrensize, 'maxgeneration': maxgeneration, 'mutprob': mutprob, 'halloffamenumber': halloffamenumber, 'indpb': indpb, 'eta': eta, 'weight1': weight1, 'weight2': weight2, 'velocityrange': velocityrange, 'heelrange': heelrange, 'lwlmin': lwlmin, 'lwlmax': lwlmax, 'bwlmin': bwlmin, 'bwlmax': bwlmax, 'tcmin': tcmin, 'tcmax': tcmax, 'lcbmin': lcbmin, 'lcbmax': lcbmax, 'lcfmin': lcfmin, 'lcfmax': lcfmax, 'gamethod': gamethod}, codecs.open('assets/data/parametersga.json', 'w', encoding='utf-8'), separators=(', ', ': '), sort_keys=True)
        
        #dimensionsobj = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
        #dimensions = json.loads(dimensionsobj)
        #for item in dimensions:
        #    item = str(item)
        #    if item != "category":
        #        globals()[item] = np.float(dimensions[item])
        #vboat = np.float((velocityrange[1]+velocityrange[0])/2)
        #heel = np.float((heelrange[1]+heelrange[0])/2)
        #savefile = "extracalculations"
        #results = resistance(lwl, bwl, tc, alcb, cp, cm, awp, disp, lcb, lcf, vboat, heel, savefile)
        #fields=[0, np.round(results[0],4), np.round(results[1],4), np.round(results[2],4), np.round(results[3],4), np.round(results[4],4), np.round(results[5],4), np.round(lwl,4), np.round(bwl,4), np.round(tc,4), np.round(disp,4), np.round(awp,4), np.round(lcb,4), np.round(lcf,4), np.round(results[0],4)-20000*np.round(results[5],4)]
        
        with open('assets/data/initialhull.csv','w') as fd:
            fd.write("id,Resistance,Rv,Ri,Rr,Rincli,Comfort,AVS,CS,LWL,BWL,Draft,Displacement,AWP,LCB,LCF,constraint1,constraint2,constraint3,constraint4,constraint5,constraint6,constraint7,valid"+"\n")
            writer = csv.writer(fd, delimiter=',')
            #writer.writerow(fields)
        with open('assets/data/optimizationresistance.csv','w') as fd:
            fd.write("id,Resistance,Rv,Ri,Rr,Rincli,Comfort,AVS,CS,LWL,BWL,Draft,Displacement,AWP,LCB,LCF,constraint1,constraint2,constraint3,constraint4,constraint5,constraint6,constraint7,valid"+"\n")
        start = time.time()
        result = optimize_nsgaII()
        done = time.time()
        elapsed = done-start
        file = open("assets/data/optimizationresistance.csv")
        numoffsprings = len(file.readlines())-1
        return html.Div(dbc.Alert("Optimization finished in {} seconds after generating {} offsprings".format(round(elapsed, 2), numoffsprings), color="success", style={'padding': '5px', 'display': 'inline-block'}))
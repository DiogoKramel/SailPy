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

#from optimizationfunctions import optimize_nsgaII
#from resistance import resistance

from functions import resistance
from functions import optimize_nsgaII


@app.callback(
    Output('dimensions-chosen-optimization', 'children'), 
    [Input('children-size', 'value')])
def callback(childrensize):
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
                html.P("{}m".format(round(lwl,2)), style={'display': 'inline-block', 'padding': '10px'}),
                dbc.Input(value="{}".format(round(loa*0.3048,2)), id='lwl-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),

                html.Br(), dbc.Label("Waterline beam"), html.Br(),
                dbc.Input(value="{}".format(round(lwl/5,2)), id='bwl-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(bwl,2)), style={'display': 'inline-block', 'padding': '10px'}),
                dbc.Input(value="{}".format(round(lwl/2.73,2)), id='bwl-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),

                html.Br(), dbc.Label("Draft"), html.Br(),
                dbc.Input(value="{}".format(round(bwl/15,2)), type='text', id='tc-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(tc,2)), style={'display': 'inline-block', 'padding': '10px'}),
                dbc.Input(value="{}".format(round(bwl/2.46,2)), type='text', id='tc-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),

                html.Br(),dbc.Label("Displacement"), html.Br(),
                dbc.Input(value="{}".format(round((lwl/8.50)**3,2)), type='text', id='disp-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m3".format(round(disp,2)), style={'display': 'inline-block', 'padding': '10px'}),
                dbc.Input(value="{}".format(round((lwl/4.34)**3,2)), type='text', id='disp-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
            ]),
            dbc.Col([
                dbc.Label("Waterplane area"), html.Br(),
                dbc.Input(value="{}".format(round((disp**(2/3)*3.78),2)), type='text', id='awp-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m2".format(round(awp,2)), style={'display': 'inline-block', 'padding': '10px'}),
                dbc.Input(value="{}".format(round((disp**(2/3)*12.67),2)), type='text', id='awp-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),

                html.Br(), dbc.Label("LCB"), html.Br(),
                dbc.Input(value="{}".format(round(lwl*0.418,2)), type='text', id='lcb-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(lcb,2)), style={'display': 'inline-block', 'padding': '10px'}),
                dbc.Input(value="{}".format(round(lwl*0.5,2)), type='text', id='lcb-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),

                html.Br(),dbc.Label("LCF"), html.Br(),
                dbc.Input(value="{}".format(round(lwl*0.405,2)), type='text', id='lcf-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(lcf,2)), style={'display': 'inline-block', 'padding': '10px'}),
                dbc.Input(value="{}".format(round(lwl*0.482,2)), type='text', id='lcf-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
            ])
        ])
    ])

@app.callback(
    Output('resistance-weight', 'children'),
    [Input('weight1', 'value')])
def update_output(value):
    return dbc.Label('Resistance Weight: {}'.format(value))

@app.callback(
    Output('comfort-weight', 'children'),
    [Input('weight2', 'value')])
def update_output(value):
    return dbc.Label('Comfort Ratio Weight: {}'.format(value))

@app.callback(
    Output('output-container-button', 'children'),
    [Input('export-ga', 'n_clicks'), Input('pop-size', 'value'), Input('children-size', 'value'), Input('max-generation', 'value'), Input('mut-prob', 'value'), Input('halloffame-number', 'value'), Input('indpb-value', 'value'), Input('eta_value', 'value'), Input('weight1', 'value'), Input('weight2', 'value'), Input('velocity-range', 'value'), Input('heel-range', 'value')])
def update_output(n_clicks, popsize, childrensize, maxgeneration, mutprob, halloffamenumber, indpb, eta, weight1, weight2, velocityrange, heelrange):
    if n_clicks == 0:
        json.dump({'popsize': popsize, 'childrensize': childrensize, 'maxgeneration': maxgeneration, 'mutprob': mutprob, 'halloffamenumber': halloffamenumber, 'indpb': indpb, 'eta': eta, 'weight1': weight1, 'weight2': weight2, 'velocityrange': velocityrange, 'heelrange': heelrange}, codecs.open('assets/data/parametersga.json', 'w', encoding='utf-8'), separators=(', ', ': '), sort_keys=True)
    if n_clicks == 1:
        json.dump({'popsize': popsize, 'childrensize': childrensize, 'maxgeneration': maxgeneration, 'mutprob': mutprob, 'halloffamenumber': halloffamenumber, 'indpb': indpb, 'eta': eta, 'weight1': weight1, 'weight2': weight2, 'velocityrange': velocityrange, 'heelrange': heelrange}, codecs.open('assets/data/parametersga.json', 'w', encoding='utf-8'), separators=(', ', ': '), sort_keys=True)
        dimensionsobj = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
        dimensions = json.loads(dimensionsobj)
        for item in dimensions:
            item = str(item)
            if item != "category":
                globals()[item] = np.float(dimensions[item])
        vboat = np.float((velocityrange[1]+velocityrange[0])/2)
        heel = np.float((heelrange[1]+heelrange[0])/2)
        savefile = "extracalculations"
        results = resistance(lwl, bwl, tc, alcb, cp, cm, awp, disp, lcb, lcf, vboat, heel, savefile)
        fields=[0, np.round(results[0],4), np.round(results[1],4), np.round(results[2],4), np.round(results[3],4), np.round(results[4],4), np.round(results[5],4), np.round(lwl,4), np.round(bwl,4), np.round(tc,4), np.round(disp,4), np.round(awp,4), np.round(lcb,4), np.round(lcf,4), np.round(results[0],4)-20000*np.round(results[5],4)]
        
        with open('assets/data/initialhull.csv','w') as fd:
            fd.write("id,Resistance,Rv,Ri,Rr,Rincli,Comfort,LWL,BWL,Draft,Displacement,AWP,LCB,LCF,best,constraint1,constraint2,constraint3,constraint4,valid"+"\n")
            writer = csv.writer(fd, delimiter=',')
            writer.writerow(fields)
        with open('assets/data/optimizationresistance.csv','w') as fd:
            fd.write("id,Resistance,Rv,Ri,Rr,Rincli,Comfort,LWL,BWL,Draft,Displacement,AWP,LCB,LCF,best,constraint1,constraint2,constraint3,constraint4,constraint5,valid"+"\n")
        optimize_nsgaII()
        return html.Div(dbc.Button(dcc.Link("See results >", href="/resultshull", style={'color': 'white'})))

@app.callback(
    Output('save-limits', 'children'),
    [Input('export-ga', 'n_clicks'), Input('lwl-min', 'value'), Input('lwl-max', 'value'), Input('bwl-min', 'value'), Input('bwl-max', 'value'), Input('tc-min', 'value'), Input('tc-max', 'value')])
def update_output(lwlmin, lwlmax, bwlmin, bwlmax, tcmin, tcmax):
    if n_clicks == 0:
        json.dump({'bound_low1': lwlmin, 'bound_up1': lwlmax, 'bound_low2': bwlmin, 'bound_up2': bwlmax, 'bound_low4': tcmin, 'bound_up4': tcmax}, codecs.open('assets/data/parametersga.json', 'w', encoding='utf-8'), separators=(', ', ': '), sort_keys=True)
    if n_clicks == 1:
        json.dump({'bound_low1': lwlmin, 'bound_up1': lwlmax, 'bound_low2': bwlmin, 'bound_up2': bwlmax, 'bound_low4': tcmin, 'bound_up4': tcmax}, codecs.open('assets/data/parametersga.json', 'w', encoding='utf-8'), separators=(', ', ': '), sort_keys=True)
        return "ok"
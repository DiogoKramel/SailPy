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
    Output('output-button', 'children'),
    [Input('export-ga', 'n_clicks'), Input('lwl-min', 'value')], [State('pop-size', 'value'), State('children-size', 'value'), State('max-generation', 'value'), State('mut-prob', 'value'), State('halloffame-number', 'value'), State('indpb-value', 'value'), State('eta_value', 'value'), State('weight1', 'value'), State('weight2', 'value'), State('velocity-range', 'value'), State('heel-range', 'value'), State('lwl-max', 'value'), State('bwl-min', 'value'), State('bwl-max', 'value'), State('tc-min', 'value'), State('tc-max', 'value'), State('lcb-min', 'value'), State('lcb-max', 'value'), State('lcf-min', 'value'), State('lcf-max', 'value')])
def update_output(n_clicks, lwlmin, popsize, childrensize, maxgeneration, mutprob, halloffamenumber, indpb, eta, weight1, weight2, velocityrange, heelrange, lwlmax, bwlmin, bwlmax, tcmin, tcmax, lcbmin, lcbmax, lcfmin, lcfmax):
    if n_clicks == 1:
        json.dump({'popsize': popsize, 'childrensize': childrensize, 'maxgeneration': maxgeneration, 'mutprob': mutprob, 'halloffamenumber': halloffamenumber, 'indpb': indpb, 'eta': eta, 'weight1': weight1, 'weight2': weight2, 'velocityrange': velocityrange, 'heelrange': heelrange, 'lwlmin': lwlmin, 'lwlmax': lwlmax, 'bwlmin': bwlmin, 'bwlmax': bwlmax, 'tcmin': tcmin, 'tcmax': tcmax, 'lcbmin': lcbmin, 'lcbmax': lcbmax, 'lcfmin': lcfmin, 'lcfmax': lcfmax}, codecs.open('assets/data/parametersga.json', 'w', encoding='utf-8'), separators=(', ', ': '), sort_keys=True)
        
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
            fd.write("id,Resistance,Rv,Ri,Rr,Rincli,Comfort,LWL,BWL,Draft,Displacement,AWP,LCB,LCF,best,constraint1,constraint2,constraint3,constraint4,valid"+"\n")
            writer = csv.writer(fd, delimiter=',')
            #writer.writerow(fields)
        with open('assets/data/optimizationresistance.csv','w') as fd:
            fd.write("id,Resistance,Rv,Ri,Rr,Rincli,Comfort,LWL,BWL,Draft,Displacement,AWP,LCB,LCF,best,constraint1,constraint2,constraint3,constraint4,constraint5,constraint6,constraint7,valid"+"\n")
        start = time.time()
        result=optimize_nsgaII()
        done = time.time()
        elapsed = done-start
        return html.Div(dbc.Alert("Done in {} seconds".format(elapsed), color="success", style={'padding': '5px'}))
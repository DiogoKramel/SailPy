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
from functions import vpp
from functions import optimization_deap_appendages
from functions import optimization_platypus_vpp


@app.callback(
    Output('resistance-weight-2', 'children'),
    [Input('weight1', 'value')])
def resistance_weight(value):
    return dbc.Label(': {}'.format(value))

@app.callback(
    Output('comfort-weight-2', 'children'),
    [Input('weight2', 'value')])
def comfort_weight(value):
    return dbc.Label(': {}'.format(value))

@app.callback(Output('output-button-2', 'children'), [Input('export-ga-2', 'n_clicks')], [State('pop-size', 'value'), State('children-size', 'value'), State('max-generation', 'value'), State('mut-prob', 'value'), State('halloffame-number', 'value'), State('indpb-value', 'value'), State('eta_value', 'value'), State('weight1', 'value'), State('weight2', 'value'), State('wind-speed-range', 'value'), State('wind-angle-range', 'value'), State('ga-method', 'value')])
def update_output(n_clicks, popsize, childrensize, maxgeneration, mutprob, halloffamenumber, indpb, eta, weight1, weight2, windspeedrange, windanglerange, gamethod):
    if n_clicks == 1:
        json.dump({'popsize': popsize, 'childrensize': childrensize, 'maxgeneration': maxgeneration, 'mutprob': mutprob, 'halloffamenumber': halloffamenumber, 'indpb': indpb, 'eta': eta, 'weight1': weight1, 'weight2': weight2, 'windspeedrange': windspeedrange, 'windanglerange': windanglerange, 'gamethod': gamethod}, codecs.open('assets/data/parametersga-appendages.json', 'w', encoding='utf-8'), separators=(', ', ': '), sort_keys=True)
        
        with open('assets/data/initialhull2.csv','w') as fd:
            fd.write("id,AverageVelocity,Comfort"+"\n")
            #writer = csv.writer(fd, delimiter=',')
            #writer.writerow(fields)
        with open('assets/data/optimizationvpp.csv','w') as fd:
            fd.write("id,AverageVelocity,AverageVelocityUpwind,Comfort,valid"+"\n")
        start = time.time()
        optimization_platypus_vpp()
        done = time.time()
        elapsed = done-start
        file = open("assets/data/optimizationvpp.csv")
        numoffsprings = len(file.readlines())-1
        return html.Div(dbc.Alert("Optimization finished in {} seconds after generating {} offsprings".format(round(elapsed, 2), numoffsprings), color="success", style={'padding': '5px', 'display': 'inline-block'}))
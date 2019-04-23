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
from functions import optimization_deap_resistance
from functions import optimization_platypus_resistance


@app.callback(Output('option-optimization', 'children'), [Input('type-optimization', 'value')])
def optionoptimization(typeoptimization):
    if typeoptimization == 'custom':
        return html.Div([
            html.Span(dbc.Label("Population size"), id="tooltip-population"),
            dbc.Tooltip("A set of individuals randomly generated to start the simulation.", target="tooltip-population"),
            dbc.Input(
                type='number', 
                id='pop-size', 
                value='10', 
                bs_size="sm", 
                style={'width': 80}),
            html.Span(dbc.Label("Number of offsprings"), id="tooltip-children"),
            dbc.Tooltip("The number of children to be produced at each generation as a result of crossover among its parents or mutation.", target="tooltip-children"),
            dbc.Input(
                type='number', 
                id='children-size', 
                value='4', 
                bs_size="sm", 
                style={'width': 80}),
            html.Span(dbc.Label("Maximum number of generations"), id="tooltip-generations"),
            dbc.Tooltip("The number of times parents will produce offsprings before an internal criteria are reached.", target="tooltip-generations"),
            dbc.Input(
                type='number', 
                id='max-generation', 
                value='15', 
                bs_size="sm", 
                style={'width': 80}),
            dbc.Label("Number of best fitting individuals selected"),
            dbc.Input(
                type='number', 
                id='halloffame-number', 
                value='5', 
                bs_size="sm", 
                style={'width': 80}),
            dbc.Label("Mutation probability for an offspring [%]"),
            dbc.Input(
                type='number', 
                id='mut-prob', 
                value='20', 
                bs_size="sm", 
                style={'width': 80}),
            dbc.Label("Independent probability for each attribute to be mutated [%]"),
            dbc.Input(
                type='number', 
                id='indpb-value', 
                value='20', 
                bs_size="sm", 
                style={'width': 80}),
            html.Span(dbc.Label("Crowding degree of the crossover [%]"), id="tooltip-crowding"),
            dbc.Tooltip("A high value will produce children resembling their parents, while a small value will produce solutions much more different.", target="tooltip-crowding"),
            dbc.Input(
                type='number', 
                id='eta_value', 
                value='20', 
                bs_size="sm", 
                style={'width': 80}),
            dbc.Label("Method of Crossover"),
            dcc.Dropdown(
                id='crossover-method', 
                options=[
                    {'label': 'Simulated Binary Bounded', 'value': '1'},
                    {'label': 'One-Point', 'value': '2'},
                    {'label': 'Two-Point', 'value': '3'},
                    {'label': 'Uniform', 'value': '4'},
                ],
                value='1',
                style={'width': '80%', 'font-size': '10pt'}
            ),
            dbc.Label("Method of Mutation"),
            dcc.Dropdown(
                id='mutation-method', 
                options=[
                    {'label': 'Polynomial Bounded', 'value': '1'},
                    {'label': 'Gaussian', 'value': '2'},
                ],
                value='1',
                style={'width': '80%', 'font-size': '10pt'}
            ),
            dbc.Label("Method of Selection"),
            dcc.Dropdown(
                id='selection-method', 
                options=[
                    {'label': 'NSGA-II', 'value': '1'},
                    {'label': 'SPEA-II', 'value': '2'},
                ],
                value='1',
                style={'width': '80%', 'font-size': '10pt'}
            ),
            html.Br(),
            html.Div(id='estimative-offspring'),
            html.A('Read More about DEAP', href='https://deap.readthedocs.io/en/master/', target="_blank"),
            dbc.Input(
                type='number', 
                id='offsprings-platypus', 
                value='300', 
                bs_size="sm", 
                style={'width': 80, 'display': 'none'}
            ),
            dcc.Dropdown(
                id='ga-method',
                options=[
                    {'label': 'NSGAII', 'value': 'NSGAII'},
                ],
                style={'width': '90%', 'font-size': '10pt', 'display': 'none'}
            ),
        ])
    
    elif typeoptimization == 'default':
        return html.Div([
            dbc.Label("Method"),
            dcc.Dropdown(
                id='ga-method',
                options=[
                    {'label': 'NSGAII - Nondominated Sorting Genetic Algorithm', 'value': 'NSGAII'},
                    {'label': 'GDE3 - Generalized Differential Evolution', 'value': 'GDE3'},
                    {'label': 'OMOPSO - Multi-Objective Particle Swarm Optimization', 'value': 'OMOPSO'},
                    {'label': 'SMPSO - Speed-Constrained Particle Swarm Optimization', 'value': 'SMPSO'},
                    {'label': 'SPEA2 - Strength Pareto Evolutionary Algorithm', 'value': 'SPEA2'},
                    {'label': 'MOEA -  Multi-Objective Evolutionary Algorithm', 'value': 'EpsMOEA'},
                ],
                value='NSGAII',
                style={'width': '100%', 'font-size': '10pt'}
            ),
            dbc.Label("Number of offsprings"),
            dbc.Input(
                type='number', 
                id='offsprings-platypus', 
                value='300', 
                bs_size="sm", 
                style={'width': '25%'}
            ),
            html.Br(),
            dbc.Label("Behave of each algorithm"),
            html.Img(src='/assets/static/platypus3.png', width='100%'),
            #### HIDDEN BELOW
            dbc.Input(
                type='number', 
                id='pop-size', 
                value='10', 
                bs_size="sm", 
                style={'width': 80, 'display': 'none'}),
            dbc.Input(
                type='number', 
                id='children-size', 
                value='4', 
                bs_size="sm", 
                style={'width': 80, 'display': 'none'}),
            dbc.Input(
                type='number', 
                id='max-generation', 
                value='15', 
                bs_size="sm", 
                style={'width': 80, 'display': 'none'}),
            dbc.Input(
                type='number', 
                id='halloffame-number', 
                value='5', 
                bs_size="sm", 
                style={'width': 80, 'display': 'none'}),
            dbc.Input(
                type='number', 
                id='mut-prob', 
                value='20', 
                bs_size="sm", 
                style={'width': 80, 'display': 'none'}),
            dbc.Input(
                type='number', 
                id='indpb-value', 
                value='20', 
                bs_size="sm", 
                style={'width': 80, 'display': 'none'}),
            dbc.Input(
                type='number', 
                id='eta_value', 
                value='20', 
                bs_size="sm", 
                style={'width': 80, 'display': 'none'}),
            dcc.Dropdown(
                id='crossover-method', 
                options=[
                    {'label': 'Simulated Binary Bounded', 'value': '1'},
                    {'label': 'One-Point', 'value': '2'},
                    {'label': 'Two-Point', 'value': '3'},
                    {'label': 'Uniform', 'value': '4'},
                ],
                value='1',
                style={'width': '80%', 'font-size': '10pt', 'display': 'none'}
            ),
            dcc.Dropdown(
                id='mutation-method', 
                options=[
                    {'label': 'Polynomial Bounded', 'value': '1'},
                    {'label': 'Gaussian', 'value': '2'},
                ],
                value='1',
                style={'width': '80%', 'font-size': '10pt', 'display': 'none'}
            ),
            dcc.Dropdown(
                id='selection-method', 
                options=[
                    {'label': 'NSGA-II', 'value': '1'},
                    {'label': 'SPEA-II', 'value': '2'},
                ],
                value='1',
                style={'width': '80%', 'font-size': '10pt', 'display': 'none'}
            ),
        ])

@app.callback(Output('estimative-offspring', 'children'), [Input('pop-size', 'value'), Input('children-size', 'value'), Input('max-generation', 'value'), Input('mut-prob', 'value')])
def resistance_weight(popsize, childrensize, maxgeneration, mutprob):
    offsprings = np.float(popsize)*np.float(childrensize)*np.float(maxgeneration)*np.float(mutprob)/100+2
    offsprings = offsprings*2
    return dbc.Label('Number of offsprings generated: {} offsprings'.format(np.int(offsprings)))

@app.callback(
    Output('resistance-weight', 'children'),
    [Input('weight1', 'value')])
def resistance_weight(value):
    return dbc.Label('Resistance Weight: {}'.format(value))

@app.callback(
    Output('comfort-weight', 'children'),
    [Input('weight2', 'value')])
def comfort_weight(value):
    return dbc.Label('Comfort Ratio Weight: {}'.format(value))

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
                dbc.Row([dbc.Label("Waterline length")]),
                dbc.Row([dbc.Input(value="{}".format(round(lwl*0.9,2)), id='lwl-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(lwl,2)), style={'display': 'inline-block', 'padding': '5px'}),
                dbc.Input(value="{}".format(round(lwl*1.1,2)), id='lwl-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ]),

                dbc.Row([dbc.Label("Waterline beam")]),
                dbc.Row([dbc.Input(value="{}".format(round(lwl/5,2)), id='bwl-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(bwl,2)), style={'display': 'inline-block', 'padding': '5px'}),
                dbc.Input(value="{}".format(round(lwl/2.73,2)), id='bwl-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ]),

                dbc.Row([dbc.Label("Draft")]),
                dbc.Row([dbc.Input(value="{}".format(round(lwl/21,2)), type='text', id='tc-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(tc,2)), style={'display': 'inline-block', 'padding': '5px'}),
                dbc.Input(value="{}".format(round(bwl/2.46,2)), type='text', id='tc-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ]),

                dbc.Row([dbc.Label("LCB")]),
                dbc.Row([dbc.Input(value="{}".format(round(lwl*0.418,2)), type='text', id='lcb-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                html.P("{}m".format(round(lcb,2)), style={'display': 'inline-block', 'padding': '5px'}),
                dbc.Input(value="{}".format(round(lwl*0.5,2)), type='text', id='lcb-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ]),
                
                dbc.Row(dbc.Label("LCF")),
                dbc.Row([
                    dbc.Input(value="{}".format(round(lwl*0.405,2)), type='text', id='lcf-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                    html.P("{}m".format(round(lcf,2)), style={'display': 'inline-block', 'padding': '5px'}),
                    dbc.Input(value="{}".format(round(lwl*0.482,2)), type='text', id='lcf-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ])

            ]),
            dbc.Col([
                dbc.Row(dbc.Label("Block Coefficient (Cb)")),
                dbc.Row([
                    dbc.Input(value="{}".format(round(0.3,2)), type='text', id='cb-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                    html.P(" - ", style={'display': 'inline-block', 'padding': '5px'}),
                    dbc.Input(value="{}".format(round(0.4,2)), type='text', id='cb-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ]),
                dbc.Row(dbc.Label("Waterplane Coefficient (Cwp)")),
                dbc.Row([
                    dbc.Input(value="{}".format(round(0.68,2)), type='text', id='cwp-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                    html.P(" - ", style={'display': 'inline-block', 'padding': '5px'}),
                    dbc.Input(value="{}".format(round(0.71,2)), type='text', id='cwp-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ]),
                dbc.Row(dbc.Label("Prismatic Coefficient (Cp)")),
                dbc.Row([
                    dbc.Input(value="{}".format(round(0.52,2)), type='text', id='cp-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                    html.P(" - ", style={'display': 'inline-block', 'padding': '5px'}),
                    dbc.Input(value="{}".format(round(0.6,2)), type='text', id='cp-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ]),
                dbc.Row(dbc.Label("Midship Area Coefficient (Cm)")),
                dbc.Row([
                    dbc.Input(value="{}".format(round(0.65,2)), type='text', id='cm-min', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                    html.P(" - ", style={'display': 'inline-block', 'padding': '5px'}),
                    dbc.Input(value="{}".format(round(0.78,2)), type='text', id='cm-max', bs_size="sm", style={'width': '30%', 'display': 'inline-block'}),
                ])
            ])
        ])
    ])

@app.callback(Output('output-button', 'children'), [Input('export-ga', 'n_clicks')], [State('pop-size', 'value'), State('children-size', 'value'), State('max-generation', 'value'), State('mut-prob', 'value'), State('halloffame-number', 'value'), State('indpb-value', 'value'), State('eta_value', 'value'), State('weight1', 'value'), State('weight2', 'value'), State('velocity-range', 'value'), State('heel-range', 'value'), State('lwl-min', 'value'), State('lwl-max', 'value'), State('bwl-min', 'value'), State('bwl-max', 'value'), State('tc-min', 'value'), State('tc-max', 'value'), State('lcb-min', 'value'), State('lcb-max', 'value'), State('disp-min', 'value'), State('lcf-min', 'value'), State('lcf-max', 'value'), State('crossover-method', 'value'), State('mutation-method', 'value'), State('selection-method', 'value'), State('capsize-factor', 'value'), State('offsprings-platypus', 'value'), State('ga-method', 'value'), State('type-optimization', 'value'), State('cb-min', 'value'), State('cb-max', 'value'), State('cwp-min', 'value'), State('cwp-max', 'value'), State('cp-min', 'value'), State('cp-max', 'value'), State('cm-min', 'value'), State('cm-max', 'value')])
def update_output(n_clicks, popsize, childrensize, maxgeneration, mutprob, halloffamenumber, indpb, eta, weight1, weight2, velocityrange, heelrange, lwlmin, lwlmax, bwlmin, bwlmax, tcmin, tcmax, lcbmin, lcbmax, dispmin, lcfmin, lcfmax, crossovermethod, mutationmethod, selectionmethod, capsizefactor, offspringsplatypus, gamethod, typeoptimization, cbmin, cbmax, cwpmin, cwpmax, cpmin, cpmax, cmmin, cmmax):
    if n_clicks >= 1:
        with open('assets/data/optimizationresistance.csv','w') as fd:
            fd.write("id,Resistance,Rv,Ri,Rr,Rincli,Comfort,CS,LWL,BWL,Draft,Displacement,AWP,LCB,LCF,constraint1,constraint2,constraint3,constraint4,constraint5,constraint6,constraint7,valid"+"\n")
        
        # initial hull
        dim_obj = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
        dim = json.loads(dim_obj) 
        lwl = np.float(dim["lwl"])
        bwl = np.float(dim["bwl"])
        tc = np.float(dim["tc"])
        alcb = np.float(dim["alcb"])
        cp = np.float(dim["cp"])
        cm = np.float(dim["cm"])
        awp = np.float(dim["awp"])
        disp = np.float(dim["disp"])
        lcf = np.float(dim["lcf"])
        lcb = np.float(dim["lcb"])
        Rt = 0
        CR = 0
        Rv = 0
        Ri = 0
        Rr =0
        Rincli =0
        count = 0
        for velocity in range (velocityrange[0], velocityrange[1], 1):
            for heel in range (heelrange[0], heelrange[1], 5):
                result = resistance(lwl, bwl, tc, alcb, cp, cm, awp, disp, lcb, lcf, velocity, heel)
                Rt = Rt+result[0]
                Rv = Rv+result[1]
                Ri = Ri+result[2]
                Rr = Rr+result[3]
                Rincli = Rincli+result[4]
                CR = CR+result[5]
                count = count+1
        Rt = Rt/count
        CR = CR/count
        Rv = Rv/count
        Ri = Ri/count
        Rr = Rr/count
        boa = bwl*1.1
        dispmass = disp*1025
        cs = boa*3.28084/(dispmass*2.20462/64)**(1/3)
        exportdata = [1, format(Rt, '.4f'), format(Rv, '.4f'), format(Ri, '.4f'), format(Rr, '.4f'), format(Rincli, '.4f'), format(CR, '.4f'), format(cs, '.4f'), format(lwl, '.4f'), format(bwl, '.4f'), format(tc, '.4f'), format(disp, '.4f'), format(awp, '.4f'), format(lcb, '.4f'), format(lcf, '.4f'), False, False, False, False, False, False, False, False]
        with open("assets/data/optimizationresistance.csv", "a") as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(exportdata)
        
        
        # optimization process
        start = time.time()
        if typeoptimization == 'default':
            json.dump({'cbmin': cbmin, 'cbmax': cbmax, 'cwpmin': cwpmin, 'cwpmax': cwpmax, 'cpmin': cpmin, 'cpmax': cpmax, 'cmmin': cmmin, 'cmmax': cmmax, 'weight1': weight1, 'weight2': weight2, 'velocityrange': velocityrange, 'heelrange': heelrange, 'lwlmin': lwlmin, 'lwlmax': lwlmax, 'bwlmin': bwlmin, 'bwlmax': bwlmax, 'tcmin': tcmin, 'tcmax': tcmax, 'lcbmin': lcbmin, 'lcbmax': lcbmax, 'lcfmin': lcfmin, 'lcfmax': lcfmax, 'capsize-factor': capsizefactor, 'offspringsplatypus': offspringsplatypus, 'gamethod': gamethod, 'dispmin': dispmin}, codecs.open('assets/data/parametersga.json', 'w', encoding='utf-8'), separators=(', ', ': '), sort_keys=True)
            result = optimization_platypus_resistance()
        elif typeoptimization == 'custom':
            json.dump({'cbmin': cbmin, 'cbmax': cbmax, 'cwpmin': cwpmin, 'cwpmax': cwpmax, 'cpmin': cpmin, 'cpmax': cpmax, 'cmmin': cmmin, 'cmmax': cmmax, 'popsize': popsize, 'childrensize': childrensize, 'maxgeneration': maxgeneration, 'mutprob': mutprob, 'halloffamenumber': halloffamenumber, 'indpb': indpb, 'eta': eta, 'weight1': weight1, 'weight2': weight2, 'velocityrange': velocityrange, 'heelrange': heelrange, 'lwlmin': lwlmin, 'lwlmax': lwlmax, 'bwlmin': bwlmin, 'bwlmax': bwlmax, 'tcmin': tcmin, 'tcmax': tcmax, 'lcbmin': lcbmin, 'lcbmax': lcbmax, 'lcfmin': lcfmin, 'lcfmax': lcfmax, 'crossovermethod': crossovermethod, 'mutationmethod': mutationmethod, 'selectionmethod': selectionmethod, 'capsize-factor': capsizefactor, 'gamethod': 'NSGA II', 'dispmin': dispmin}, codecs.open('assets/data/parametersga.json', 'w', encoding='utf-8'), separators=(', ', ': '), sort_keys=True)
            result = optimization_deap_resistance(np.float(dispmin))
        done = time.time()
        elapsed = done-start
        file = open("assets/data/optimizationresistance.csv")
        numoffsprings = len(file.readlines())-2
        return html.Div(dbc.Alert("Optimization finished in {} seconds after generating {} offsprings".format(round(elapsed, 2), numoffsprings), color="success", style={'padding': '5px', 'display': 'inline-block'}))

@app.callback(Output('disp-tc-min', 'children'), [Input('velocity-range', 'value')])
def limits_lcb(lwl):
    dimensionsobj = codecs.open('assets/data/dimensions.json', 'r', encoding='utf-8').read()
    dimensions = json.loads(dimensionsobj)
    lwl = np.float(dimensions["lwl"])
    dispmin = (np.float(lwl)/5.5)**3
    return html.Div([
        dbc.Label("Minimum Displacement"),
        dbc.Input(
            type='text', 
            id='disp-min', 
            value=round(dispmin, 2), 
            bs_size="sm", 
            style={'width': 80}),
    ])
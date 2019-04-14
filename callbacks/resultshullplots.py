import dash
import numpy as np
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_daq as daq
from app import app
import plotly.graph_objs as go
import json, codecs
from scipy.integrate import simps
import csv
import pandas as pd


@app.callback(Output('output-optimization', 'figure'), [Input('resultshullaxisy', 'value'), Input('resultshullaxisx', 'value')])
def update_output(resultshullaxisy, resultshullaxisx):
    df = pd.read_csv("assets/data/optimizationresistance.csv")
    dfinit = pd.read_csv("assets/data/initialhull.csv")
    
    # calculate pareto frontier
    def pareto_frontier(Xs, Ys, maxX = True, maxY = True):
        myList = sorted([[Xs[i], Ys[i]] for i in range(len(Xs))], reverse=maxX)
        p_front = [myList[0]]    
        
        for pair in myList[1:]:
            if maxY: 
                if pair[1] >= p_front[-1][1]:
                    p_front.append(pair)
            else:
                if pair[1] <= p_front[-1][1]:
                    p_front.append(pair)
        p_frontX = [pair[0] for pair in p_front]
        p_frontY = [pair[1] for pair in p_front]
        return p_frontX, p_frontY
    
    dfvalid = df.loc[df['valid']==True]
    dfvalid=dfvalid.reset_index()
    dfnotvalid = df.loc[df["valid"]==False]
    p_front = pareto_frontier(dfvalid["Comfort"], dfvalid["Resistance"], maxX = True, maxY = False)
    paretox=[]
    paretoy=[]
    paretoname=[]
    if (resultshullaxisx == "Comfort" and resultshullaxisy == "Resistance"):
        paretox=p_front[0]
        paretoy=p_front[1]
        paretoname='Pareto'
    elif (resultshullaxisx == "Resistance" and resultshullaxisy == "Comfort"):
        paretoy=p_front[0]
        paretox=p_front[1]
        paretoname='Pareto'
    else:
        paretox=dfinit[resultshullaxisx]
        paretoy=dfinit[resultshullaxisy]
        paretoname="Initial hull"

    return {
        'data': [
            go.Scatter(
                x=dfvalid[resultshullaxisx],
                y=dfvalid[resultshullaxisy],
                text=dfvalid["id"],
                textposition='top center',
                mode='markers',
                name='Valid individuals',
                marker=dict(
                    cmax=max(df["id"]),
                    cmin=1,
                    color=df["id"],
                    colorbar=dict(
                        title='Offspring'
                    ),
                    colorscale='Viridis',
                    opacity = 0.5+0.5*df["id"]/max(df["id"]),
                ),
            ),
            go.Scatter(
                x=dfnotvalid[resultshullaxisx],
                y=dfnotvalid[resultshullaxisy],
                text=dfnotvalid["id"],
                textposition='top center',
                mode='markers',
                name='Invalid',
                marker=dict(
                    color='rgba(255,0,0,0.2)',
                    symbol='cross',
                ),
            ),
            go.Scatter(
                x=dfinit[resultshullaxisx],
                y=dfinit[resultshullaxisy],
                text=dfinit["id"],
                textposition='top center',
                mode='markers',
                name='Initial hull',
                marker=dict(
                    symbol='star',
                ),
            ),
            go.Scatter(
                x=paretox,
                y=paretoy,
                mode='lines',
                name=paretoname,
                line = dict(dash = 'dash'),
            ),
            ],
        'layout': go.Layout(
            title="NSGA II Optimization",
            height=500,
            hovermode="closest",
            margin={
                "r": 20,
                "t": 30,
                "b": 50,
                "l": 50
            },
            xaxis={
                "autorange": True,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": resultshullaxisx,
            },
            yaxis={
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": resultshullaxisy,
                "range": [min(df[resultshullaxisy]), max(df[resultshullaxisy])],
            },
        legend=dict(x=0.8, y=1),
        font=dict(size=12),
        )
    }

@app.callback(
    Output('plot-constraint-individual', 'children'),
    [Input('output-optimization', 'hoverData')])
def update_y_timeseries(hoverData):
    df = pd.read_csv("assets/data/optimizationresistance.csv")
    hover = np.int(hoverData["points"][0]['text'])
    row = df.loc[df['id']==hover]
    avs = np.float(row.iloc[0]['AVS'])
    cs = np.float(row.iloc[0]['CS'])
    return html.Div([
        dbc.Label("Angle of Vanishing Stability: {} degrees".format(round(avs,2))),
        html.Br(),
        dbc.Label("Capsize Screening Factor: {}".format(round(cs,2))),
        html.Br(),
    ])

@app.callback(
    Output('plot-resistance-individual', 'figure'),
    [Input('output-optimization', 'hoverData')])
def update_y_timeseries(hoverData):
    df = pd.read_csv("assets/data/optimizationresistance.csv")
    hover = np.int(hoverData["points"][0]['text'])
    row = df.loc[df['id']==hover]
    Rv = [row.iloc[0]['Rv']]
    Ri = [row.iloc[0]['Ri']]
    Rr = [row.iloc[0]['Rr']]
    Rincli = [row.iloc[0]['Rincli']]
    return {
        'data': [
            go.Bar(
                x=['R'],
                y=Rv,
                name = "Viscous",
                marker=dict(
                    color='rgb(43,140,190)'
                ),
            ),
            go.Bar(
                x=['R'],
                y=Ri,
                name = "Induced",
                marker=dict(
                    color='rgb(123,204,196)'
                )
            ),
            go.Bar(
                x=['R'],
                y=Rr,
                name = "Residual",
                marker=dict(
                    color='rgb(186,228,188)'
                ),
            ),
            go.Bar(
                x=['R'],
                y=Rincli,
                name = "Inclination",
                marker=dict(
                    color='rgb(240,249,232)'
                ),
            ),
            ],
        'layout': go.Layout(
            barmode="stack",
            title="Resistance",
            hovermode="closest",
            height=600,
            margin={
                "r": 20,
                "t": 30,
                "b": 50,
                "l": 50
            },
            yaxis={
                "title": "Resistance Components",
            },
        legend=dict(x=-.1, y=-0.3),
        font=dict(size=10),
        )
    }

@app.callback(Output('plot-limits-lwl-bwl', 'figure'), [Input('output-optimization', 'hoverData')])
def update_y_timeseries(hoverData):
    df = pd.read_csv("assets/data/optimizationresistance.csv")
    dfinit = pd.read_csv("assets/data/initialhull.csv")
    xmin = min(df["BWL"])
    xmax = max(df["BWL"])
    hover = np.int(hoverData["points"][0]['text'])
    row = df.loc[df['id']==hover]
    return {
        'data': [
            go.Scatter(
                x=df["BWL"],
                y=df["LWL"],
                text=df["id"],
                textposition='top center',
                mode='markers',
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[xmin*2.73, xmax*2.73],
                mode='lines',
                line = dict(color = 'red', dash = 'dash'),
                fill='tozeroy',
                fillcolor='rgba(255,0,0,0.2)',
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[xmin*5, xmax*5],
                mode='lines',
                line = dict(color = 'red', dash = 'dash'),
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[xmax*7, xmax*7],
                mode='lines',
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(
                    color='red', 
                    dash='dash'
                ),
            ),
            go.Scatter(
                x=dfinit["BWL"],
                y=dfinit["LWL"],
                mode='markers',
                marker = dict(color = 'green', symbol = 'star'),
            ),
            go.Scatter(
                x=[row.iloc[0]['BWL']],
                y=[row.iloc[0]['LWL']],
                marker=dict(
                    color='orange',
                    symbol='cross'
                ),
            ),
            ],
        'layout': go.Layout(
            height=200,
            hovermode="closest",
            showlegend=False,
            margin={
                "r": 10,
                "t": 20,
                "b": 30,
                "l": 30
            },
            xaxis={
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Waterline beam",
                "range": [xmin, xmax],
            },
            yaxis={
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Waterline length",
                "range": [xmin*2.5, xmax*5.5],
            },
        font=dict(size=10),
        )
    }

@app.callback(
    dash.dependencies.Output('plot-limits-bwl-tc', 'figure'),
    [Input('output-optimization', 'hoverData')])
def update_y_timeseries(hoverData):
    df = pd.read_csv("assets/data/optimizationresistance.csv")
    dfinit = pd.read_csv("assets/data/initialhull.csv")
    xmin = min(df["BWL"])
    xmax = max(df["BWL"])
    hover = np.int(hoverData["points"][0]['text'])
    row = df.loc[df['id']==hover]
    return {
        'data': [
            go.Scatter(
                x=df["BWL"],
                y=df["Draft"],
                text=df["id"],
                textposition='top center',
                mode='markers',
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[xmin/2.46, xmax/2.46],
                mode='lines',
                line = dict(color = 'red', dash = 'dash'),
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[xmax/2, xmax/2],
                mode='lines',
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(
                    color='red', 
                    dash='dash'
                ),
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[xmin/19.38, xmax/9.38],
                mode='lines',
                line = dict(color = 'red', dash = 'dash'),
                fill='tozeroy',
                fillcolor='rgba(255,0,0,0.2)',
            ),
            go.Scatter(
                x=dfinit["BWL"],
                y=dfinit["Draft"],
                mode='markers',
                marker = dict(color = 'green', symbol = 'star'),
            ),
            go.Scatter(
                x=[row.iloc[0]['BWL']],
                y=[row.iloc[0]['Draft']],
                marker=dict(
                    color='orange',
                    symbol='cross'
                ),
            ),
            ],
        'layout': go.Layout(
            height=200,
            hovermode="closest",
            showlegend=False,
            margin={
                "r": 10,
                "t": 20,
                "b": 30,
                "l": 30
            },
            xaxis={
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Waterline beam",
                "range": [xmin, xmax],
            },
            yaxis={
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Draft",
                "range": [0, xmax/2.4]
            },
        font=dict(size=10),
        )
    }

@app.callback(
    dash.dependencies.Output('plot-limits-lwl-disp', 'figure'),
    [Input('output-optimization', 'hoverData')])
def update_y_timeseries(hoverData):
    df = pd.read_csv("assets/data/optimizationresistance.csv")
    dfinit = pd.read_csv("assets/data/initialhull.csv")
    xmin = min(df["LWL"])
    xmax = max(df["LWL"])
    hover = np.int(hoverData["points"][0]['text'])
    row = df.loc[df['id']==hover]
    return {
        'data': [
            go.Scatter(
                x=df["LWL"],
                y=df["Displacement"],
                text=df["id"],
                textposition='top center',
                mode='markers',
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[(xmin/4.34)**3, (xmax/4.34)**3],
                mode='lines',
                line = dict(color = 'red', dash = 'dash'),
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[(xmax/4)**3, (xmax/4)**3],
                mode='lines',
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(
                    color='red', 
                    dash='dash'
                ),
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[(xmin/8.5)**3, (xmax/8.5)**3],
                fill='tozeroy',
                fillcolor='rgba(255,0,0,0.2)',
                mode='lines',
                line = dict(color = 'red', dash = 'dash'),
            ),
            go.Scatter(
                x=dfinit["LWL"],
                y=dfinit["Displacement"],
                mode='markers',
                marker = dict(color = 'green', symbol = 'star'),
            ),
            go.Scatter(
                x=[row.iloc[0]['LWL']],
                y=[row.iloc[0]['Displacement']],
                marker=dict(
                    color='orange',
                    symbol='cross'
                ),
            ),
            ],
        'layout': go.Layout(
            height=200,
            hovermode="closest",
            showlegend=False,
            margin={
                "r": 10,
                "t": 20,
                "b": 30,
                "l": 30
            },
            xaxis={
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Waterline length",
                "range": [xmin, xmax]
            },
            yaxis={
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Displacement",
                "range": [0, (xmax/4.3)**3],
            },
        font=dict(size=10),
        )
    }

@app.callback(
    dash.dependencies.Output('plot-limits-awp-disp', 'figure'),
    [Input('output-optimization', 'hoverData')])
def update_y_timeseries(hoverData):
    df = pd.read_csv("assets/data/optimizationresistance.csv")
    dfinit = pd.read_csv("assets/data/initialhull.csv")
    xmin = min(df["AWP"])
    xmax = max(df["AWP"])
    hover = np.int(hoverData["points"][0]['text'])
    row = df.loc[df['id']==hover]
    return {
        'data': [
            go.Scatter(
                x=df["AWP"],
                y=df["Displacement"],
                text=df["id"],
                textposition='top center',
                mode='markers',
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[(xmin/3.78)**(3/2), (xmax/3.78)**(3/2)],
                mode='lines',
                line = dict(color = 'red', dash = 'dash'),
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[(xmax/3)**(3/2), (xmax/3)**(3/2)],
                mode='lines',
                fill='tonexty',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(
                    color='red', 
                    dash='dash'
                ),
            ),
            go.Scatter(
                x=[xmin, xmax],
                y=[(xmin/12.67)**(3/2), (xmax/12.67)**(3/2)],
                mode='lines',
                line = dict(color = 'red', dash = 'dash'),
                fill='tozeroy',
                fillcolor='rgba(255,0,0,0.2)',
            ),
            go.Scatter(
                x=dfinit["AWP"],
                y=dfinit["Displacement"],
                mode='markers',
                marker = dict(color = 'green', symbol = 'star'),
            ),
            go.Scatter(
                x=[row.iloc[0]['AWP']],
                y=[row.iloc[0]['Displacement']],
                marker=dict(
                    color='orange',
                    symbol='cross'
                ),
            ),
            ],
        'layout': go.Layout(
            height=200,
            hovermode="closest",
            showlegend=False,
            margin={
                "r": 10,
                "t": 20,
                "b": 30,
                "l": 30
            },
            xaxis={
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Waterplane area",
                "range": [xmin, xmax],
            },
            yaxis={
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Displacement",
                "range":[0, (xmax/3.7)**(3/2)],
            },
        font=dict(size=10),
        )
    }

@app.callback(
     Output('plot-parallel-dimensions', 'figure'),
    [Input('parallel-datatype', 'value')])
def update_output(type):
    print(type)
    if np.float(type) == 1:
        df = pd.read_csv("assets/data/optimizationresistance.csv")
    elif np.float(type) == 2:
        df = pd.read_csv("assets/data/optimizationresistance.csv")
        df = df.loc[df['valid']==True]
    elif np.float(type) == 3:
        df = pd.read_csv("assets/data/optimizationresistance.csv")
        df = df.loc[df['valid']==False]
    return {
        'data': [
            go.Parcoords(
                line = dict(
                    color=df["id"],
                    colorscale = 'Viridis',
                    showscale = True,
                    cmin=1,
                    cmax=max(df["id"]),
                    colorbar=dict(
                        title='Generation'
                    ),
                ),
                dimensions = list([
                    dict(label = 'Waterline Length [m]', values = df['LWL']),
                    dict(label = 'Waterline Beam [m]', values = df['BWL']),
                    dict(label = 'Draft [m]', values = df['Draft']),
                    dict(label = 'Displacement [m3]', values = df['Displacement']),
                    dict(label = 'Waterplane area [m2]', values = df['AWP']),
                    dict(label = 'LCB [m]', values = df['LCB']),
                    dict(label = 'LCF [m]', values = df['LCF']),
                ]),
            ),
        ],
        'layout': go.Layout(
            title="Dimension set per hull",
            hovermode="closest",
            margin={
                "r": 20,
                "t": 100,
                "b": 50,
                "l": 50
            },
            font=dict(size=12),
        )
    }
datatable_all = pd.read_csv("assets/data/optimizationresistance.csv")
datatable_valid = datatable_all.loc[datatable_all['valid']==True]
datatable_unvalid = datatable_all.loc[datatable_all['valid']==False]

@app.callback(Output("plot-dimensions", "children"), [Input("resultshullaxisx", "value"), Input('datatable-interactivity', 'selected_rows')])
def update_graph(resultshullaxisx, selected_row_indices):
    if selected_row_indices is None:
        selected_row_indices = []
    return html.Div([
            dcc.Graph(
                id=column,
                figure={
                    'data': [
                        go.Bar(
                            x=datatable_valid["id"],
                            y=datatable_valid[column] if column in datatable_valid else [],
                            name='Valid',
                        ),
                        go.Bar(
                            x=datatable_unvalid["id"],
                            y=datatable_unvalid[column] if column in datatable_unvalid else [],
                            marker=dict(color='red'),
                            name='Not valid',
                        ),
                        go.Bar(
                            x=datatable_all["id"].iloc[selected_row_indices],
                            y=datatable_all[column].iloc[selected_row_indices] if column in datatable_unvalid else [],
                            marker=dict(color='green'),
                            name='Selected',
                        ),
                    ],
                    "layout": {
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 100,
                        "margin": {"t": 30, "l": 10, "r": 10, "b":0},
                        "title": column,
                        'font': dict(size=9),
                        'barmode': 'overlay'
                    },	
                },
            )
            for column in ["LWL", "BWL", "Draft", "Resistance", "Comfort"]
        ]
    )

@app.callback(Output("export-hull-dimensions", "children"), [Input("dropdown-hull-dimensions", "value")])
def update_y_timeseries(id):
    df = pd.read_csv("assets/data/optimizationresistance.csv")
    row = df.iloc[np.int(id)]
    bwl = df.iloc[np.int(id)]['BWL']
    lwl = df.iloc[np.int(id)]['LWL']
    tc = df.iloc[np.int(id)]['Draft']
    lcb = df.iloc[np.int(id)]['LCB']
    lcf = df.iloc[np.int(id)]['LCF']
    disp = df.iloc[np.int(id)]['Displacement']
    json.dump({'lwl': lwl, 'bwl': bwl, 'tc': tc, 'disp': disp, 'lcb': lcb, 'lcf': lcf}, codecs.open('assets/data/dimensions-hull.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)
    return html.Div([
            dbc.Alert("Exported hull number {}".format(id), color="success", style={'padding': '5px', 'display': 'inline-block'}),
            html.P("Waterline Length: {}m -- Waterline Beam: {}m -- Draft: {}m".format(round(np.float(lwl),2), round(np.float(bwl),2), round(np.float(tc),2)), style={'padding-left': '20px', 'display': 'inline-block'})
        ])
    
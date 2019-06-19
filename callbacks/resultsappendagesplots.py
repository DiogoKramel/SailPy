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


@app.callback(Output('output-optimization2', 'figure'), [Input('resultshullaxisy', 'value'), Input('resultshullaxisx', 'value')])
def update_output(resultshullaxisy, resultshullaxisx):
    df = pd.read_csv("assets/data/optimizationvpp.csv")
    #dfinit = pd.read_csv("assets/data/initialhull.csv")
    
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
    #dfnotvalid = df.loc[df["valid"]==False]
    p_front = pareto_frontier(dfvalid["Comfort"], dfvalid["AverageVelocity"], maxX = True, maxY = True)
    
    paretox=[]
    paretoy=[]
    paretoname=[]
    if (resultshullaxisx == "Comfort" and resultshullaxisy == "AverageVelocity"):
        paretox=p_front[0]
        paretoy=p_front[1]
        paretoname='Pareto'
    elif (resultshullaxisx == "AverageVelocity" and resultshullaxisy == "Comfort"):
        paretoy=p_front[0]
        paretox=p_front[1]
        paretoname='Pareto'
    #else:
    #    paretox=dfinit[resultshullaxisx]
    #    paretoy=dfinit[resultshullaxisy]
    #    paretoname="Initial hull"

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
            #go.Scatter(
            #    x=dfnotvalid[resultshullaxisx],
            #    y=dfnotvalid[resultshullaxisy],
            #    text=dfnotvalid["id"],
            #    textposition='top center',
            #    mode='markers',
            #    name='Invalid',
            #    marker=dict(
            #        color='rgba(255,0,0,0.2)',
            #        symbol='cross',
            #    ),
            #),
            #go.Scatter(
            #    x=dfinit[resultshullaxisx],
            #    y=dfinit[resultshullaxisy],
            #    text=dfinit["id"],
            #    textposition='top center',
            #    mode='markers',
            #    name='Initial hull',
            #    marker=dict(
            #        symbol='star',
            #    ),
            #),
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
            height=380,
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
        legend=dict(x=0.5, y=1),
        font=dict(size=12),
        )
    }


@app.callback(Output('polar-diagram', 'figure'), [Input('output-optimization2', 'hoverData')])
def callback_vpp(hoverData):
    hover = np.int(hoverData["points"][0]['text'])
    index = np.str(hover)
    filename="assets/data/vpp_results/veloc_hull_"+index+".json"
    
    veloc_obj = codecs.open(filename, 'r', encoding='utf-8').read()
    veloc_solution = json.loads(veloc_obj)
    velocities= np.asarray(veloc_solution['velocity_boat_matrix_list'])
    ymax=1.1*np.max(velocities)

    angles_obj = codecs.open("assets/data/vpp_results/angles.json", 'r', encoding='utf-8').read()
    angles_solution = json.loads(angles_obj)
    angles= np.asarray(angles_solution['angle'])
    return {
        'data': [go.Scatterpolar(
            theta=angles,
            r=velocities[0],
            mode='lines',
            name='6 knots'
        ),
        go.Scatterpolar(
            theta=angles,
            r=velocities[1],
            mode='lines',
            name='8 knots'
        ), 
        go.Scatterpolar(
            theta=angles,
            r=velocities[2],
            mode='lines',
            name='10 knots'
        ),
        go.Scatterpolar(
            theta=angles,
            r=velocities[3],
            mode='lines',
            name='12 knots'
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
                    range = [0, ymax],
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

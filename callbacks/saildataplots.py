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


@app.callback(Output('output-optimization-sd', 'figure'), [Input('resultshullaxisy', 'value'), Input('resultshullaxisx', 'value'), Input('year-interval', 'value'), Input('rig-type', 'value'), Input('keel-type', 'value')])
def update_output(resultshullaxisy, resultshullaxisx, yearinterval, rigtype, keeltype):
    df = pd.read_csv("assets/data/saildata.csv")
    if rigtype != None:
        df = df.loc[df['typerig']==rigtype]
    return {
        'data': [
            go.Scatter(
                x=df[resultshullaxisx],
                y=df[resultshullaxisy],
                text=df["name"]+" by "+df["designer"],
                textposition='top center',
                mode='markers',
                name='Valid individuals',
            ),
            ],
        'layout': go.Layout(
            title="Sail Data",
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
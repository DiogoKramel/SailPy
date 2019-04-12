import dash
import numpy as np
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app
import plotly.graph_objs as go
import json, codecs
from scipy.integrate import simps

from functions import keel_solve, sac_solve, section_solve, wl_solve


@app.callback(Output('insert-sac', 'figure'), [Input('lwl', 'value'), Input('cb', 'value'), Input('lcb', 'value'), Input('alpha_f_sac', 'value'), Input('alpha_i_sac', 'value'), Input('beamtransom', 'value'), Input('bwl', 'value'), Input('tc', 'value'), Input('cm', 'value')])
def create_sac(lwl, cb, lcb, alpha_f_sac, alpha_i_sac, beamtransom, bwl, tc, cm):
    sac_solution = sac_solve(np.float(lwl), np.float(cb), np.float(lcb), np.float(alpha_f_sac), np.float(alpha_i_sac), np.float(beamtransom), np.float(bwl), np.float(tc), np.float(cm)),
    return {
        'data': [
            go.Scatter(
                x = sac_solution[0][0],
                y = sac_solution[0][1],
                name = "Control points",
                line = dict(dash = 'dash', color = "rgba(58, 124, 211)"),
                marker = dict(color = "rgb(46, 117, 211)"),
                cliponaxis = False,
            ),
            go.Scatter(
                x = sac_solution[0][2],
                y = sac_solution[0][3],
                mode = "lines",
                name = "Spline",
                line = dict(color = "rgba(236, 45, 45, 0.5)"),
                fill = 'tozeroy',
            ),
            go.Scatter(
                x = [np.float(lcb)],
                y = [0],
                text = "LCB",
                textposition = ["top center"],
                mode = "markers+text",
                name = "LCB",
                line = dict(color = "rgb(46, 117, 211)"),
                cliponaxis=False,
            ),
            go.Scatter(
                x = [sac_solution[0][5]],
                y = [sac_solution[0][4]],
                text = "SAC max",
                textposition = ["top center"],
                mode = "markers+text",
                name = "Maximum SAC",
                line = dict(color = "rgb(46, 117, 211)"),
                cliponaxis = False,
            ),
        ],
        'layout': go.Layout(
            title='Sectional Areas Curve',
            height = 300,
            hovermode = "closest",
            margin = {
                "r": 20,
                "t": 30,
                "b": 50,
                "l": 50
            },
            xaxis = {
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Length [m]",
                "zeroline": False,
                "range": [-1, np.float(lwl)*1.1],
            },
            yaxis = {
                "autorange": False,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Sectional Area [m<sup>2</sup>]",
                "range": [0, sac_solution[0][1][2]*1.2],
            },
            legend=dict(x=0, y=-0.3, orientation="h"),
            font=dict(size=10),
            
        )
    }

@app.callback(Output('insert-wl', 'figure'), [Input('lcf', 'value'), Input('cwp', 'value'), Input('lwl', 'value'), Input('beamtransom', 'value'), Input('bwl', 'value')])
def create_wl(lcf, cwp, lwl, beamtransom, bwl):
    wl_solution = wl_solve(np.float(lcf), np.float(cwp), np.float(lwl), np.float(beamtransom), np.float(bwl)),
    return {
        'data': [
            go.Scatter(
                x = wl_solution[0][0],
                y = wl_solution[0][1],
                name = "Control points",
                line = dict(dash = 'dash', color = "rgb(46, 117, 211)"),
                marker = dict(color = "rgb(46, 117, 211)"),
                cliponaxis = False,
            ),
            go.Scatter(
                x = wl_solution[0][2],
                y = wl_solution[0][3],
                mode = "lines",
                name = "Spline",
                line = dict(color = "rgba(236, 45, 45, 0.5)"),
                fill = 'tozeroy'
            ),
            go.Scatter(
                x = [np.float(lcf)],
                y = [0],
                text = ["LCF"],
                textposition = ["top center"],
                mode = "markers+text",
                line = dict(color = "rgb(46, 117, 211)"),
                name = "LCF",
                cliponaxis = False,
            ),
            go.Scatter(
                x = [wl_solution[0][5]],
                y = [wl_solution[0][4]],
                text = ["BWL max"],
                textposition = ["top center"],
                mode = "markers+text",
                line = dict(color= "rgb(46, 117, 211)"),
                name = "Maximum beam at waterline",
                cliponaxis = False,
            ),
        ],
        'layout': go.Layout(
            title='Waterline Curve',
            height = 200,
            hovermode = "closest",
            margin = {
                "r": 20,
                "t": 30,
                "b": 50,
                "l": 50
            },
            xaxis = {
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Length [m]",
                "zeroline": False,
                "range": [-1, np.float(lwl)*1.1],
            },
            yaxis = {
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Half Beam [m]",
                "zeroline": False,
                "range": [0, max(wl_solution[0][1])*1.2],
            },
            legend=dict(x=0, y=-0.6, orientation="h"),
            font=dict(size=10),
        )
    }

@app.callback(Output('insert-keel', 'figure'), [Input('lwl', 'value'), Input('tc', 'value')])
def create_keel(lwl, tc):
    keel_solution = keel_solve(np.float(lwl), np.float(tc)),
    return {
        'data': [
            go.Scatter(
                x = keel_solution[0][0],
                y = keel_solution[0][1],
                name = "Control points",
                line = dict(dash = 'dash', color = "rgb(46, 117, 211)"),
                marker = dict(color = "rgb(46, 117, 211)"),
                cliponaxis = False,
            ),
            go.Scatter(
                x = keel_solution[0][2],
                y = keel_solution[0][3],
                mode = "lines",
                name = "Spline",
                line = dict(color= "rgba(236, 45, 45, 0.5)"),
                fill = 'tozeroy'
            ),
            go.Scatter(
                x = [keel_solution[0][4]],
                y = [-np.float(tc)],
                text = ["Tc max"],
                textposition = ["top center"],
                mode = "markers+text",
                marker = dict(color= "rgb(46, 117, 211)"),
                name = "Maximum canoe body draft",
                cliponaxis=False,
            ),
        ],
        'layout': go.Layout(
            title='Profile Curve',
            height = 200,
            hovermode = "closest",
            margin = {
                "r": 20,
                "t": 30,
                "b": 50,
                "l": 50
            },
            xaxis = {
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Length [m]",
                "range": [-1, np.float(lwl)*1.1],
                "zeroline": False,
            },
            yaxis = {
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Draft [m]",
                "zeroline": False,
                "range": [keel_solution[0][1][1]*1.2, 0],
            },
            legend=dict(x=0, y=-0.6, orientation="h"),
            font=dict(size=10),
        )
    }

@app.callback(Output('insert-section', 'figure'), [Input('lwl', 'value'), Input('beta_n', 'value'), Input('cb', 'value'), Input('lcb', 'value'), Input('alpha_f_sac', 'value'), Input('alpha_i_sac', 'value'), Input('beamtransom', 'value'), Input('bwl', 'value'), Input('tc', 'value'), Input('cm', 'value'), Input('lcf', 'value'), Input('cwp', 'value')])
def create_section(lwl, beta_n, cb, lcb, alpha_f_sac, alpha_i_sac, beamtransom, bwl, tc, cm, lcf, cwp):
    sn_sections_sol = sac_solve(np.float(lwl), np.float(cb), np.float(lcb), np.float(alpha_f_sac), np.float(alpha_i_sac), np.float(beamtransom), np.float(bwl), np.float(tc), np.float(cm)),
    sn_sections = sn_sections_sol[0][6]
    bn_sections_sol = wl_solve(np.float(lcf), np.float(cwp), np.float(lwl), np.float(beamtransom), np.float(bwl))
    bn_sections = bn_sections_sol[6]
    tn_sections_sol = keel_solve(np.float(lwl), np.float(tc))
    tn_sections = tn_sections_sol[5]
    section_solution = section_solve(tn_sections, bn_sections, sn_sections, np.float(lwl), np.float(beta_n)),
    return {
        'data': [
            go.Scatter(
                x = -section_solution[0][1][0],
                y = section_solution[0][2][0],
                name = "Section 10",
                mode = 'lines',
                cliponaxis = False,
            ),
            go.Scatter(
                x = -section_solution[0][1][1],
                y = section_solution[0][2][1],
                name = "Section 9",
                mode = 'lines',
                cliponaxis = False,
            ),
            go.Scatter(
                x = -section_solution[0][1][2],
                y = section_solution[0][2][2],
                name = "Section 8",
                mode = 'lines',
                cliponaxis = False,
            ),
            go.Scatter(
                x = -section_solution[0][1][3],
                y = section_solution[0][2][3],
                name = "Section 7",
                mode = 'lines',
                cliponaxis = False,
            ),
            go.Scatter(
                x = -section_solution[0][1][4],
                y = section_solution[0][2][4],
                name = "Section 6",
                mode = 'lines',
                cliponaxis = False,
            ),
            go.Scatter(
                x = section_solution[0][1][5],
                y = section_solution[0][2][5],
                name = "Section 5",
                mode = 'lines',
                cliponaxis = False,
            ),
            go.Scatter(
                x = section_solution[0][1][6],
                y = section_solution[0][2][6],
                name = "Section 4",
                mode = 'lines',
                cliponaxis = False,
            ),
            go.Scatter(
                x = section_solution[0][1][7],
                y = section_solution[0][2][7],
                name = "Section 3",
                mode = 'lines',
                cliponaxis = False,
            ),
            go.Scatter(
                x = section_solution[0][1][8],
                y = section_solution[0][2][8],
                name = "Section 2",
                mode = 'lines',
                cliponaxis = False,
            ),
            go.Scatter(
                x = section_solution[0][1][9],
                y = section_solution[0][2][9],
                name = "Section 1",
                mode = 'lines',
                cliponaxis = False,
            ),
        ],
        'layout': go.Layout(
            title = "Body Plan",
            height = 300,
            hovermode = "closest",
            margin = {
                "r": 20,
                "t": 30,
                "b": 50,
                "l": 50
            },
            xaxis = {
                "autorange": True,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": 'Beam [m]',
                "zeroline": False,
            },
            yaxis = {
                "autorange": True,
                "linewidth": 1,
                "showgrid": True,
                "showline": True,
                "mirror": True,
                "title": "Draft [m]",
                "zeroline": False,
            },
            annotations=[
                dict(
                    x=0.5,
                    y=0.1,
                    showarrow=False,
                    text='Bow'),
                dict(
                    x=-0.5,
                    y=0.1,
                    showarrow=False,
                    text='Stern'),
            ],
            legend=dict(x=0, y=-0.4, orientation="h"),
            font=dict(size=10),
        )
    }
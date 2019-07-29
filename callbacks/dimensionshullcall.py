import dash
from app import app
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
import json, codecs
import numpy as np
from scipy.integrate import simps
import pandas as pd

from functions import keel_solve, sac_solve, section_solve, wl_solve


@app.callback(Output('loa-ft', 'children'), [Input('loa', 'value')])
def loa_ft(loa):
    return ': {} ft'.format(loa)

@app.callback(Output('main-dimensions', 'children'), [Input('loa', 'value')])
def main_dimensions(loa):
    lwl = loa*0.3048*0.85
    bwl = 0.115*lwl+2.1667
    if lwl < 10:
        bwl = 0.155*lwl+2.1667
    tc = lwl/18
    lcb = (50-3.29)/100*lwl
    lcf = (50-6.25)/100*lwl
    return html.Details([
        html.Summary('Main Dimensions'),
        html.Div([
            dbc.Label('Waterline Length [m]'),
            dbc.Input(type='text', id='lwl', bs_size='sm', value='{}'.format(round(lwl,2))),
            html.Div(id='limits-lwl', className='limits'),
            dbc.Label('Waterline Beam [m]'),
            dbc.Input(type='text', id='bwl', bs_size='sm', value='{}'.format(round(bwl,2))),
            dbc.Label('Draft Canoe Body [m]'),
            dbc.Input(type='text', id='tc', bs_size='sm', value='{}'.format(round(tc,2))),
            html.Div(id='limits-tc', className='limits'),
            dbc.Label('Longitudinal Centre of Buoyancy (LCB) [m]'),
            dbc.Input(type='text', id='lcb', bs_size='sm', value='{}'.format(round(lcb,2))),
            html.Div(id='limits-lcb', className='limits'),
            dbc.Label('Longitudinal Centre of Flotation (LCF) [m]'),
            dbc.Input(type='text', id='lcf', bs_size='sm', value='{}'.format(round(lcf,2))),
            html.Div(id='limits-lcf', className='limits'),
            dbc.Label('Beam at the Transom [m]'),
            dbc.Input(type='text', id='beamtransom', bs_size='sm', value='0'),
            html.Br(),
        ], className='regularfont'),
    ])

# Source: Illuminati
@app.callback(Output('limits-lwl', 'children'), [Input('loa', 'value')])
def limits_lwl(loa): 
    lwlmin = (np.float(loa)*0.7-2)/3.2804
    lwlest = (np.float(loa)*0.8)/3.2804
    lwlmax = (np.float(loa)*0.9+1.079)/3.2804
    return 'Minimum: {}'.format(round(lwlmin,2)), ' -- Recommended: {}'.format(round(lwlest,2)), ' -- Maximum: {}'.format(round(lwlmax,2))

# Source: DELFT series
@app.callback(Output('limits-lcf', 'children'), [Input('lwl', 'value')])
def limits_lcf(lwl):
    lcfmin = np.float(lwl)*0.405
    lcfmax = np.float(lwl)*0.482
    return 'Minimum: {} -'.format(round(lcfmin,2)), '- Maximum: {}'.format(round(lcfmax,2)),

# Source: DELFT series
@app.callback(Output('limits-lcb', 'children'), [Input('lwl', 'value')])
def limits_lcb(lwl):
    lcbmin = np.float(lwl)*0.42
    lcbmax = np.float(lwl)*0.5
    return 'Minimum: {} -'.format(round(lcbmin,2)), '- Maximum: {}'.format(round(lcbmax,2)),

# Source: DELFT series
@app.callback(Output('limits-tc', 'children'), [Input('loa', 'value')])
def limits_tc(loa):
    tcmin = ((np.float(loa)*0.8+1.079)/3.2804)/22
    tcmax = ((np.float(loa)*0.7-2)/3.2804)/13
    return 'Minimum: {} -'.format(round(tcmin,2)),'- Maximum: {}'.format(round(tcmax,2))



@app.callback(Output('test-lwlbwl', 'children'), [Input('lwl', 'value'), Input('bwl', 'value')])
def test_lwlbwl(lwl, bwl):
    lwlbwl = np.float(lwl)/np.float(bwl)
    if lwlbwl > 5 or lwlbwl < 2.73:
        successfail = 'danger'
        alert = 'Out of limits'
    else:
        successfail = 'success'
        alert = 'Within limits'
    return dbc.Row([
        dbc.Col('1) Length/Beam Ratio: {}'.format(round(lwlbwl,2)), width=6), 
        dbc.Col('Limits: 2.73 - 5.00', width=4), 
        dbc.Col(dbc.Alert('{}'.format(alert), color='{}'.format(successfail), style={'padding': '2px', 'display': 'inline-block'}))
    ])

@app.callback(Output('test-bwltc', 'children'), [Input('tc', 'value'), Input('bwl', 'value')])
def test_bwltc(tc, bwl):
    bwltc=np.float(bwl)/np.float(tc)
    if bwltc > 19.38 or bwltc < 2.46:
        successfail = 'danger'
        alert = 'Out of limits'
    else:
        successfail = 'success'
        alert = 'Within limits'
    return dbc.Row([
        dbc.Col('2) Beam/Draft Ratio: {}'.format(round(bwltc,2)), width=6), 
        dbc.Col('Limits: 2.46 - 19.38', width=4), 
        dbc.Col(dbc.Alert('{}'.format(alert), color='{}'.format(successfail), style={'padding': '2px', 'display': 'inline-block'}))
    ])

@app.callback(Output('test-lwldisp', 'children'), [Input('lwl', 'value'), Input('bwl', 'value'), Input('tc', 'value'), Input('cb', 'value')])
def test_lwldisp(lwl, bwl, tc, cb):
    disp = np.float(lwl)*np.float(bwl)*np.float(tc)*np.float(cb)
    lwldisp = np.float(lwl)/disp**(1/3)
    if lwldisp > 8.5  or lwldisp < 4.34:
        successfail = 'danger'
        alert = 'Out of limits'
    else:
        successfail = 'success'
        alert = 'Within limits'
    return dbc.Row([
        dbc.Col('3) Length/Displacement Factor: {}'.format(round(lwldisp,2)), width=6), 
        dbc.Col('Limits: 4.34 - 8.50', width=4), 
        dbc.Col(dbc.Alert('{}'.format(alert), color='{}'.format(successfail), style={'padding': '2px', 'display': 'inline-block'}))
    ])

@app.callback(Output('test-loadingfactor', 'children'), [Input('cwp', 'value'), Input('cb', 'value'), Input('lwl', 'value'), Input('bwl', 'value'), Input('tc', 'value')])
def test_loadingfactor(cwp, cb, lwl, bwl, tc):
    loadingfactor = (np.float(cwp)*np.float(lwl)*np.float(bwl))/(np.float(cb)*np.float(lwl)*np.float(bwl)*np.float(tc))**(2/3)
    if loadingfactor > 12.67 or loadingfactor < 3.78:
        successfail = 'danger'
        alert = 'Out of limits'
    else:
        successfail = 'success'
        alert = 'Within limits'
    return dbc.Row([
        dbc.Col(
            html.Span(
                dbc.Label('4) Loading Factor: {}'.format(round(loadingfactor,2))), 
            id="loading-factor"),
        width=6),
        dbc.Tooltip("Ratio between Waterplane Area and Displacement", target="loading-factor"),
        dbc.Col('Limits: 3.78 - 12.67', width=4), 
        dbc.Col(dbc.Alert('{}'.format(alert), color='{}'.format(successfail), style={'padding': '2px', 'display': 'inline-block'}))
    ])

@app.callback(Output('test-prismatic', 'children'), [Input('cb', 'value'), Input('bwl', 'value'), Input('lwl', 'value'), Input('tc', 'value'), Input('cm', 'value')])
def test_prismatic(cb, bwl, lwl, tc, cm):
    prismatic = np.float(cb)*np.float(lwl)*np.float(tc)*np.float(bwl)/(np.float(bwl)*np.float(tc)*np.float(cm)*np.float(lwl))
    if prismatic > 0.6 or prismatic < 0.52:
        successfail = 'danger'
        alert = 'Out of limits'
    else:
        successfail = 'success'
        alert = 'Within limits'
    return dbc.Row([
        dbc.Col('5) Prismatic Coefficient: {}'.format(round(prismatic,2)), width=6), 
        dbc.Col('Limits: 0.52 - 0.6', width=4), 
        dbc.Col(dbc.Alert('{}'.format(alert), color='{}'.format(successfail), style={'padding': '2px', 'display': 'inline-block'}))
    ])

@app.callback(Output('test-feasibility', 'children'), [Input('cwp', 'value'), Input('bwl', 'value'), Input('lwl', 'value'), Input('cb', 'value'), Input('tc', 'value'), Input('cm', 'value')])
def test_feasibility(cwp, bwl, lwl, cb, tc, cm):
    lwl = np.float(lwl)
    bwl = np.float(bwl)
    tc = np.float(tc)
    cb = np.float(cb)
    cwp = np.float(cwp)
    cm = np.float(cm)
    disp = lwl*bwl*tc*cb
    awp = lwl*bwl*cwp
    sacmax = bwl*tc*cm
    prismatic = disp/(sacmax*lwl)
    loadingfactor = awp/disp**(2/3)
    lwldisp = lwl/disp**(1/3)
    bwltc = bwl/tc
    lwlbwl = lwl/bwl
    if prismatic > 0.6 or prismatic < 0.52 or lwlbwl > 5 or lwlbwl < 2.73 or bwltc > 19.38 or bwltc < 2.46 or lwldisp > 8.5 or lwldisp < 4.34 or loadingfactor > 12.67 or loadingfactor < 3.78:
        successfail = 'danger'
        alert = 'The study sailboat may not be feasible. Consider changing the dimensions'
    else:
        successfail = 'success'
        alert = 'The study sailboat is feasible. You can proceed'
    return dbc.Alert('{}'.format(alert), color='{}'.format(successfail), style={'padding': '5pt'})

style={}
@app.callback(Output('other-dimensions', 'children'), [Input('lwl','value'), Input('bwl','value'), Input('cb', 'value'), Input('cwp', 'value'), Input('lcf', 'value'), Input('lcb', 'value'), Input('tc', 'value'), Input('cm', 'value'), Input('beta_n', 'value'), Input('beta_n2', 'value')])
def other_dimensions(lwl, bwl, cb, cwp, lcf, lcb, tc, cm, beta_n, beta_n2):
    cwp = np.float(cwp)
    cm = np.float(cm)
    cb = np.float(cb)
    lwl = np.float(lwl)
    bwl = np.float(bwl)
    tc = np.float(tc)
    lcf = np.float(lcf)
    
    sac_obj = codecs.open('assets/data/sacsolution.json', 'r', encoding='utf-8').read()
    sac_solution = json.loads(sac_obj)
    sac_interpolation_x = np.asarray(sac_solution['x_i_sac'])
    sac_interpolation_y = np.asarray(sac_solution['y_i_sac'])
    
    wl_obj = codecs.open('assets/data/wlsolution.json', 'r', encoding='utf-8').read()
    wl_solution = json.loads(wl_obj)
    waterline_interpolation_y = np.asarray(wl_solution['y_i_wl'])
    waterline_interpolation_x = np.asarray(wl_solution['x_i_wl'])

    keel_obj = codecs.open('assets/data/keelsolution.json', 'r', encoding='utf-8').read()
    keel_solution = json.loads(keel_obj)
    keel_interpolation_y = np.asarray(keel_solution['y_i_keel'])
    keel_interpolation_x = np.asarray(keel_solution['x_i_keel'])

    awp = cwp*lwl*bwl
    disp = cb*lwl*bwl*tc
    am = cm*bwl*tc # mid section area
    cp = disp/(am*lwl)
    # surface area of canoe body by Larsson pag 33
    scb = 0        
    for i in range (1,(len(sac_interpolation_x)-1)):
        if (i%2) == 0:
            scb = scb+sac_interpolation_y[i]*2
        else:
            scb = scb+sac_interpolation_y[i]*4
    scb = 2*1.03*np.float(scb)*(lwl/(len(sac_interpolation_y)-1))/3
    # lateral area of canoe body
    alcb = -simps(keel_interpolation_y, keel_interpolation_x)
    # transverse moment of inertia according to Larsson pag 39
    itwp = 0
    for i in range (1,(len(waterline_interpolation_y)-1)):
        if (i%2)==0:
            itwp = itwp+waterline_interpolation_y[i]**3*2
        else:
            itwp = itwp+waterline_interpolation_y[i]**3*4
    itwp = 2/9*np.float(itwp)*lwl/(len(waterline_interpolation_y)-1)
    # itwp = cwp**2/11.7*lwl*bwl**3 # empirical method
    # longitudinal moment of inertia
    itwplong=0
    for i in range (1,(len(waterline_interpolation_y)-1)):
        if (i%2)==0:
            itwplong = itwplong+2*waterline_interpolation_y[i]*waterline_interpolation_x[i]**2
        else:
            itwplong = itwplong+4*waterline_interpolation_y[i]*waterline_interpolation_x[i]**2
    itwplong = 2/3*np.float(itwplong)*lwl/(len(waterline_interpolation_y)-1)-awp*lcf**2
    bmt = itwp/disp
    bmlong = itwplong/disp
    kb = tc*(5/6-cb/(3*cwp))     # source
    kg = 0.1                     # is it a good guess?
    gmt = kb+bmt-kg
    gmlong = kb+bmlong-kg

    #coefficient to estimate alcb during resistance calculation
    alcb_coefficient = alcb/(lwl*tc)
    
    json.dump({'alcb': alcb, 'lwl': lwl, 'disp': disp, 'awp': awp, 'lcf': lcf, 'lcb': lcb, 'tc': tc, 'beta_n': beta_n, 'beta_n2': beta_n2, 'cwp': cwp, 'cb': cb, 'cm': cm, 'cp': cp, 'bwl': bwl, 'scb': scb, 'am': am, 'itwp': itwp, 'bmt': bmt, 'kb': kb, 'kg': kg, 'gmt': gmt, 'gmlong': gmlong, 'alcb_coefficient': alcb_coefficient}, codecs.open('assets/data/dimensions.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)
    
    data = {'Parameters' : ['Displacement', 'Waterplane Area', 'Canoe Body Lateral Area', 'Wetted Surface Area', 'Transverse Moment of Inertia', 'Metacentric Radius', 'Vertical Centre of Buoyancy (KB)', 'Metacentric Height (GM)'], 'Values' : [round(disp,2), round(awp,2), round(alcb,2), round(scb,2), round(itwp,2), round(bmt,2), round(kg,2), round(gmt,2)], 'Unit' : ['m3', 'm2', 'm2', 'm2', 'm4', 'm', 'm', 'm']}
    df = pd.DataFrame(data)

    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("rows"),
        style_cell={'textAlign': 'center', 'minWidth': '0px', 'maxWidth': '50px', 'whiteSpace': 'normal', 'font_family': 'Source Sans Pro'},
        style_cell_conditional=[{'if': {'column_id': 'Parameters'}, 'textAlign': 'left'}],
        style_as_list_view=True,
        style_header={'fontWeight': 'bold'},
        
    )

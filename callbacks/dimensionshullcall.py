import dash
from app import app
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import json, codecs
import numpy as np
from scipy.integrate import simps
import plotly.graph_objs as go  #DELETE

from functions import keel_solve, sac_solve, section_solve, wl_solve


@app.callback(Output('loa-ft', 'children'), [Input('loa', 'value')])
def loa_ft(loa):
    return ': {} ft'.format(loa)

@app.callback(Output('main-dimensions', 'children'), [Input('boat-category', 'value'), Input('loa', 'value')])
def main_dimensions(boatcategory, loa):
    if boatcategory == 'cruiser':
        lwl = loa*0.3048*0.90
        bwl = lwl/3.219
        tc = bwl/4.324
        lcb = (50-3.29)/100*lwl
        lcf = (50-6.25)/100*lwl
    if boatcategory == 'racer':
        lwl = loa*0.3048*0.95
        bwl = lwl/3.155
        tc = bwl/3.992
        lcb = (50-2.29)/100*lwl
        lcf = (50-3.33)/100*lwl
    return html.Details([
        html.Summary('Main Dimensions'),
        html.Div([
            dbc.Label('Waterline Length [m]'),
            dbc.Input(type='text', id='lwl', bs_size='sm', value='{}'.format(round(lwl,2))),
            html.Div(id='limits-lwl', className="limits"),
            dbc.Label('Waterline Beam [m]'),
            dbc.Input(type='text', id='bwl', bs_size='sm', value='{}'.format(round(bwl,2))),
            dbc.Label('Draft Canoe Body [m]'),
            dbc.Input(type='text', id='tc', bs_size='sm', value='{}'.format(round(tc,2))),
            html.Div(id='limits-tc', className="limits"),
            dbc.Label('Longitudinal Centre of Buyoancy (LCB) [m]'),
            dbc.Input(type='text', id='lcb', bs_size='sm', value='{}'.format(round(lcb,2))),
            html.Div(id='limits-lcb', className="limits"),
            dbc.Label('Longitudinal Centre of Flotation (LCF) [m]'),
            dbc.Input(type='text', id='lcf', bs_size='sm', value='{}'.format(round(lcf,2))),
            html.Div(id='limits-lcf', className="limits"),
            dbc.Label('Beam at the Transom [m]'),
            dbc.Input(type='text', id='beamtransom', bs_size='sm', value='0'),
            html.Br(),
        ], className='regularfont'),
    ])

@app.callback(Output('form-coefficients', 'children'), [Input('boat-category', 'value')])
def form_coefficients(boatcategory):
    # estimations from DELFT series based on Sysser parent models #44 and #1
    if boatcategory == 'cruiser':
        cm = 0.72
        cb = 0.39
        cwp = 0.7
    if boatcategory == 'racer':
        cm = 0.65
        cb = 0.31
        cwp = 0.7
    return html.Details([
        html.Summary('Form Coefficients'),
        html.Div([
            dbc.Label('Midsection Coefficient'),
            dcc.Slider(
                id='cm',
                min=0.65,
                max=0.78,
                value=cm,
                step=0.01,
                marks={0.65: '0.65', 0.68: '0.68', 0.71: '0.71', 0.74: '0.74', 0.78: '0.78'}
            ),
            html.Br(),
            dbc.Label('Block Coefficient'),
            dcc.Slider(
                id='cb',
                min=0.3,
                max=0.4,
                value=cb,
                step=0.01,
                marks={0.3: '0.3', 0.32: '0.32', 0.34: '0.34', 0.36: '0.36', 0.38: '0.38', 0.4: '0.4'}
            ),
            html.Br(),
            dbc.Label('Waterplane Area Coefficient'),
            dcc.Slider(
                id='cwp',
                min=0.68,
                max=0.71,
                value=cwp,
                step=0.01,
                marks={0.68: '0.65', 0.69: '0.69', 0.70: '0.71', 0.71: '0.71'}
            ),
            html.Br(), html.Br()
        ], className='regularfont')
    ])

@app.callback(Output('hull-adjustmetns', 'children'), [Input('boat-category', 'value')])
def hull_adjustmetns(boatcategory):
    # estimations from DELFT series based on Sysser parent models #44 and #1
    # suggestion: adjust the values for very high and low overall lenghts
    if boatcategory == 'cruiser':
        angforesac = 5
        angrearsac = 25
        betan = 0
    if boatcategory == 'racer':
        angforesac = 5
        angrearsac = 25
        betan = 10
    return html.Details([
        html.Summary('Hull Adjustments'),
        html.Div([
            dbc.Label('SAC angle at the bow [degrees]'),
            dbc.Input(type='text', id='alpha_f_sac', bs_size='sm', value='{}'.format(round(angforesac,2))),
            dbc.Label('SAC angle at the stern [degrees]'),
            dbc.Input(type='text', id='alpha_i_sac', bs_size='sm', value='{}'.format(round(angrearsac,2))),
            dbc.Label('Hull bottom angle [degrees]'),
            dbc.Input(type='text', id='beta_n', bs_size='sm', value='{}'.format(round(betan,2)))
        ], className='regularfont')
    ])

# Source: Illuminati
@app.callback(Output('limits-lwl', 'children'), [Input('loa', 'value'), Input('boat-category', 'value')])
def limits_lwl(loa, boat_category): 
    if (boat_category == 'cruiser'):
        lwlmin = (np.float(loa)*0.7-2)/3.2804
        lwlest = (np.float(loa)*0.8)/3.2804
        lwlmax = (np.float(loa)*0.8+1.079)/3.2804
    elif (boat_category == 'racer'):
        lwlmin = (np.float(loa)*0.8+1.079)/3.2804
        lwlest = (np.float(loa)*0.92)/3.2804
        lwlmax = (np.float(loa))/3.2804
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
@app.callback(Output('limits-tc', 'children'), [Input('loa', 'value'), Input('boat-category', 'value')])
def limits_tc(loa, boat_category):
    if (boat_category == 'cruiser'):
        tcmin = ((np.float(loa)*0.8+1.079)/3.2804)/22
        tcmax = ((np.float(loa)*0.7-2)/3.2804)/13
    if (boat_category == 'racer'):
        tcmin = ((np.float(loa)*0.8+1.079)/3.2804)/22
        tcmax = ((np.float(loa)*0.7-2)/3.2804)/15
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
        dbc.Col('1) Length/Beam Ratio: {}'.format(round(lwlbwl,2)), width=5), 
        dbc.Col('Limits: [2.73-5.00]'), 
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
        dbc.Col('2) Beam/Draft Ratio: {}'.format(round(bwltc,2)), width=5), 
        dbc.Col('Limits: [2.46-19.38]'), 
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
        dbc.Col('3) Length/Displacement Factor: {}'.format(round(lwldisp,2)), width=5), 
        dbc.Col('Limits: [4.34-8.50]'), 
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
        dbc.Col('4) Loading Factor: {}'.format(round(loadingfactor,2)), width=5), 
        dbc.Col('Limits: [3.78-12.67]'), 
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
        dbc.Col('5) Prismatic Coefficient: {}'.format(round(prismatic,2)), width=5), 
        dbc.Col('Limits: [0.52-0.6]'), 
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
    return dbc.Alert('{}'.format(alert), color='{}'.format(successfail), style={'padding': '5pt', 'display': 'inline-block'})





@app.callback(Output('other-dimensions', 'children'), [Input('lwl','value'), Input('bwl','value'), Input('cb', 'value'), Input('cwp', 'value'), Input('lcf', 'value'), Input('lcb', 'value'), Input('tc', 'value'), Input('cm', 'value'), Input('beta_n', 'value')])
def other_dimensions(lwl, bwl, cb, cwp, lcf, lcb, tc, cm, beta_n):
    cwp = np.float(cwp)
    cm = np.float(cm)
    cb = np.float(cb)
    lwl = np.float(lwl)
    bwl = np.float(bwl)
    tc = np.float(tc)
    lcf = np.float(lcf)
    
    sac_obj = codecs.open('assets/data/sacsolution.json', 'r', encoding='utf-8').read()
    sac_solution = json.loads(sac_obj)
    sn_sections = np.asarray(sac_solution["sn_sections"])
    wl_obj = codecs.open('assets/data/wlsolution.json', 'r', encoding='utf-8').read()
    wl_solution = json.loads(wl_obj)
    bn_sections = np.asarray(wl_solution["bn_sections"])
    y_i_wl = np.asarray(wl_solution["y_i_wl"])
    x_i_wl = np.asarray(wl_solution["x_i_wl"])
    keel_obj = codecs.open('assets/data/keelsolution.json', 'r', encoding='utf-8').read()
    keel_solution = json.loads(keel_obj)
    tn_sections = np.asarray(keel_solution["tn_sections"])
    y_i_keel = np.asarray(keel_solution["y_i_keel"])
    x_i_keel = np.asarray(keel_solution["x_i_keel"])
    section_solution=section_solve(tn_sections, bn_sections, sn_sections, lwl, np.float(beta_n))
    section_y_sections=section_solution[1]
    section_z_sections=section_solution[2]

    awp = cwp*lwl*bwl
    disp = cb*lwl*bwl*tc
    am = cm*bwl*tc # mid section area
    cp = disp/(am*lwl)
    
    scb_tot = 0        # lateral area of canoe body
    for z in range(0, 10):
        for i in range (1, 10):
            scb_parc = np.sqrt((section_y_sections[z][i]-section_y_sections[z][i-1])**2+(section_z_sections[z][i]-section_z_sections[z][i-1])**2)
            scb_tot = scb_tot+scb_parc
    # CORRIGIR POR QUE *2.2??
    scb = np.float(scb_tot)/10*lwl*2*2.2
    alcb = -simps(y_i_keel, x_i_keel)
    
    '''
    sum=0
    for i in range (1,(len(y_i_wl)-1)):
        if (i%2)==0:
            sum=sum+y_i_wl[i]**3*2
        else:
            sum=sum+y_i_wl[i]**3*4
    itwp=2/3*(np.float(sum)/3*np.float(lwl)/100)
    #itwp = cwp**2/11.7*lwl*bwl**3   # transversal inertia moment
    sum=0
    for i in range (1,(len(y_i_wl)-1)):
        if (i%2)==0:
            sum=sum+2*y_i_wl[i]*x_i_wl[i]**2
        else:
            sum=sum+4*y_i_wl[i]*x_i_wl[i]**2
    itwplong=2/3*np.float(sum)*lwl/len(y_i_wl)-awp*lcf**2
    bmt = itwp/disp
    bmlong = itwplong/disp
    kb = tc*(5/6-cb/(3*cwp))     #source
    kg = 0.1                     # is it a good guess?
    gmt = kb+bmt-kg
    gmlong = kb+bmlong-kg
    
    json.dump({'alcb': alcb, 'category': boatcategory, 'loa': loa, 'lwl': lwl, 'disp': disp, 'awp': awp, 'lcf': lcf, 'lcb': lcb, 'beamtransom': beamtransom, 'tc': tc, 'alpha_f_sac': alpha_f_sac, 'alpha_i_sac': alpha_i_sac, 'beta_n': beta_n, 'cwp': cwp, 'cb': cb, 'cm': cm, 'cp': cp, 'bwl': bwl, 'scb': scb, 'am': am, 'itwp': itwp, 'bmt': bmt, 'kb': kb, 'kg': kg, 'gmt': gmt, 'gmlong': gmlong}, codecs.open('assets/data/dimensions.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)
    '''
    json.dump({'lwl': lwl}, codecs.open('assets/data/dimensions.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)
    
    return html.Div([
        html.Col([
            'Displacement: {} m3'.format(round(disp,2)), html.Br(), 
            'Waterplane Area: {} m2'.format(round(awp,2)), html.Br(),
            #'Canoe Body Lateral Area: {} m2'.format(round(alcb,2)), html.Br(),
            #'Canoe Body Surface Area: {} m2'.format(round(scb,2))
        ]),
        html.Col([
            'Itwp: {} m3'.format(round(disp,2)), html.Br(), 
            'BMt: {} m3'.format(round(disp,2)), html.Br(), 
            'KB: {} m3'.format(round(disp,2)), html.Br(), 
            'GMt: {} m3'.format(round(disp,2)), html.Br(), 
        ]),
    ])
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

################################################### 
### LIMITS OF PARAMETERS
################################################### 
@app.callback(
     Output('output-loa', 'children'),
    [ Input('loa', 'value')])
def callback_bwl(loa):
    return 'h: {} ft'.format(loa)

@app.callback(
    Output('output-lwl', 'children'),
    [Input('loa', 'value'), Input('boat-category', 'value')])
def callback_lwl_limits(loa_value, boat_category):     # Source: Illuminati
    if (boat_category == 'cruiser'):
        return 'Minimum: {}'.format(round(((np.float(loa_value)*0.7-2)/3.2804),2)), ' -- Recommended: {}'.format(round(((np.float(loa_value)*0.8)/3.2804),2)), ' -- Maximum: {}'.format(round(((np.float(loa_value)*0.8+1.079)/3.2804),2))
    elif (boat_category == 'racer'):
        return 'Minimum: {}'.format(round(((np.float(loa_value)*0.8+1.079)/3.2804),2)), ' -- Recommended: {}'.format(round(((np.float(loa_value)*0.92)/3.2804),2)), ' -- Maximum: {}'.format(round(((np.float(loa_value))/3.2804),2))

@app.callback(
     Output('output-disp', 'children'),
    [ Input('loa', 'value'), Input('boat-category', 'value')])
def callback_disp_limits(loa_value, boat_category):     # Source: Illuminati
    if (boat_category == 'cruiser'):
        return 'Minimum: {} -'.format(round((np.float(loa_value)*15-257)*0.0283168),2), '- Maximum: {}'.format(round((np.float(loa_value)*3.2808*17-250)*0.0283168),2)
    elif (boat_category == 'racer'):
        return 'Minimum: {} -'.format(round((np.float(loa_value)*12-200)*0.0283168),2), '- Maximum: {}'.format(round((np.float(loa_value)*3.2808*15-257)*0.0283168),2)

@app.callback(
     Output('output-awp', 'children'),
    [ Input('disp', 'value')])
def callback_awp_limits(disp_value):    # Source: DELFT series
    return 'Minimum: {} -'.format(round(3.78*np.float(disp_value)**(2/3),2)), '- Maximum: {}'.format(round(12.67*np.float(disp_value)**(2/3),2)),

@app.callback(
     Output('output-lcf', 'children'),
    [ Input('lwl', 'value')])
def callback_lcf_limits(lwl_value):    # Source: DELFT series
    return 'Minimum: {} -'.format(round(np.float(lwl_value)*0.405,2)), '- Maximum: {}'.format(round(np.float(lwl_value)*0.482,2)),

@app.callback(
     Output('output-lcb', 'children'),
    [ Input('lwl', 'value')])
def callback_lcb_limits(lwl_value):    # Source: DELFT series
    return 'Minimum: {} -'.format(round(np.float(lwl_value)*0.42,2)), '- Maximum: {}'.format(round(np.float(lwl_value)*0.5,2)),

@app.callback(
     Output('output-tc', 'children'),
    [ Input('loa', 'value'),  Input('boat-category', 'value')])
def callback_tc_limits(loa_value, boat_category):    # Source: DELFT series
    if (boat_category == 'cruiser'):
        return 'Minimum: {} -'.format(round(((np.float(loa_value)*0.8+1.079)/3.2804)/22,2)),'- Maximum: {}'.format(round(((np.float(loa_value)*0.7-2)/3.2804)/13,2)),
    if (boat_category == 'racer'):
        return 'Minimum: {} -'.format(round(((np.float(loa_value)*0.8+1.079)/3.2804)/22,2)),'- Maximum: {}'.format(round(((np.float(loa_value)*0.7-2)/3.2804)/15,2)),


################################################### 
### TESTING FITNESS
################################################### 
@app.callback(Output('output-bwlsac', 'children'),
    [Input('awp', 'value'), Input('disp', 'value'), Input('lwl', 'value'), Input('lcf', 'value'), Input('beamtransom', 'value'), Input('tc', 'value'), Input('lcb', 'value'), Input('alpha_f_sac', 'value'), Input('alpha_i_sac', 'value')])
def callback_bwl(awp_value, disp_value, lwl_value, lcf_value, beamtransom_value, tc_value, lcb_value, alpha_f_sac_value, alpha_i_sac_value):
    sac_obj = codecs.open('data/sacsolution.json', 'r', encoding='utf-8').read()
    sac_solution = json.loads(sac_obj)
    maxsac = np.asarray(sac_solution["maxsac"])
    wl_obj = codecs.open('data/wlsolution.json', 'r', encoding='utf-8').read()
    wl_solution = json.loads(wl_obj)
    bn_sections = np.asarray(wl_solution["bn_sections"])
    bwl = np.asarray(wl_solution["bwlmax"])
    output=np.array([bwl,maxsac])
    return output

@app.callback(Output('output-lwlbwl', 'children'),
    [Input('lwl', 'value'), Input('output-bwlsac', 'children')])
def callback_bwl(lwl_value, bwlsac):
    lwlbwl=np.float(lwl_value)/np.float(bwlsac[0]*2)
    if lwlbwl > 5 or lwlbwl < 2.73:
        return dbc.Row([dbc.Col('1) Length/Beam Ratio: {}'.format(round(lwlbwl,2)), width=5), dbc.Col('Limits: [2.73-5.00]'), dbc.Col(dbc.Alert("Out of limits", color="danger", style={'padding': '2px', 'display': 'inline-block'}))])
    else:
        return dbc.Row([dbc.Col('1) Length/Beam Ratio: {}'.format(round(lwlbwl,2)), width=5), dbc.Col('Limits: [2.73-5.00]'), dbc.Col(dbc.Alert("Within limits", color="success", style={'padding': '2px', 'display': 'inline-block'}))])

@app.callback(
    Output('output-bwltc', 'children'),
    [Input('tc', 'value'), Input('output-bwlsac', 'children')])
def callback_bwl(tc_value, bwlsac):
    bwltc=np.float(bwlsac[0]*2)/np.float(tc_value)
    if bwltc > 19.38 or bwltc < 2.46:
        return dbc.Row([dbc.Col('2) Beam/Draft Ratio: {}'.format(round(bwltc,2)), width=5), dbc.Col('Limits: [2.46-19.38]'), dbc.Col(dbc.Alert("Out of limits", color="danger", style={'padding': '2px', 'display': 'inline-block'}))])
    else:
        return dbc.Row([dbc.Col('2) Beam/Draft Ratio: {}'.format(round(bwltc,2)), width=5), dbc.Col('Limits: [2.46-19.38]'), dbc.Col(dbc.Alert("Within limits", color="success", style={'padding': '2px', 'display': 'inline-block'}))])

@app.callback(
    Output('output-lwldisp', 'children'),
    [Input('lwl', 'value'), Input('disp', 'value')])
def callback_bwl(lwl_value, disp_value):
    lwldisp=(np.float(lwl_value))/np.float(disp_value)**(1/3)
    if lwldisp > 8.5 or lwldisp < 4.34:
        return dbc.Row([dbc.Col('3) Length/Displacement Factor: {}'.format(round(lwldisp,2)), width=5), dbc.Col('Limits: [4.34-8.50]'), dbc.Col(dbc.Alert("Out of limits", color="danger", style={'padding': '2px', 'display': 'inline-block'}))])
    else:
        return dbc.Row([dbc.Col('3) Length/Displacement Factor: {}'.format(round(lwldisp,2)), width=5), dbc.Col('Limits: [4.34-8.50]'), dbc.Col(dbc.Alert("Within limits", color="success", style={'padding': '2px', 'display': 'inline-block'}))])

@app.callback(
    Output('output-loadingfactor', 'children'),
    [Input('awp', 'value'), Input('disp', 'value')])
def callback_bwl(awp_value, disp_value):
    loadingfactor=np.float(awp_value)/np.float(disp_value)**(2/3)
    if loadingfactor > 12.67 or loadingfactor < 3.78:
        return dbc.Row([dbc.Col('4) Loading Factor: {}'.format(round(loadingfactor,2)), width=5), dbc.Col('Limits: [3.78-12.67]'), dbc.Col(dbc.Alert("Out of limits", color="danger", style={'padding': '2px', 'display': 'inline-block'}))])
    else:
        return dbc.Row([dbc.Col('4) Loading Factor: {}'.format(round(loadingfactor,2)), width=5), dbc.Col('Limits: [3.78-12.67]'), dbc.Col(dbc.Alert("Within limits", color="success", style={'padding': '2px', 'display': 'inline-block'}))])

@app.callback(
    Output('output-prismatic', 'children'),
    [Input('disp', 'value'), Input('bwl', 'value'), Input('lwl', 'value'), Input('tc', 'value'), Input('cm', 'value')])
def callback_bwl(disp_value, bwl, lwl_value, tc, cm):
    prismatic=np.float(disp_value)/(np.float(bwl)*np.float(tc)*np.float(cm)*np.float(lwl_value))
    if prismatic > 0.6 or prismatic < 0.52:
        return dbc.Row([dbc.Col('5) Prismatic Coefficient: {}'.format(round(prismatic,2)), width=5), dbc.Col('Limits: [0.52-0.6]'), dbc.Col(dbc.Alert("Out of limits", color="danger", style={'padding': '2px', 'display': 'inline-block'}))])
    else:
        return dbc.Row([dbc.Col('5) Prismatic Coefficient: {}'.format(round(prismatic,2)), width=5), dbc.Col('Limits: [0.52-0.6]'), dbc.Col(dbc.Alert("Within limits", color="success", style={'padding': '2px', 'display': 'inline-block'}))])

@app.callback(
    Output('output-midship', 'children'),
    [Input('cm', 'value')])
def callback_bwl(cm):
    midship=np.float(cm)
    if midship > 0.78 or midship < 0.65:
        return dbc.Row([dbc.Col('6) Midship Section Area Coefficient: {}'.format(round(midship,2)), width=5), dbc.Col('Limits: [0.65-0.78]'), dbc.Col(dbc.Alert("Out of limits", color="danger", style={'padding': '2px', 'display': 'inline-block'}))])
    else:
        return dbc.Row([dbc.Col('6) Midship Section Area Coefficient: {}'.format(round(midship,2)), width=5), dbc.Col('Limits: [0.65-0.78]'), dbc.Col(dbc.Alert("Within limits", color="success", style={'padding': '2px', 'display': 'inline-block'}))])

@app.callback(
    Output('output-cb', 'children'),
    [Input('tc', 'value'), Input('bwl', 'value'), Input('lwl', 'value'), Input('disp', 'value')])
def callback_bwl(tc_value, bwl, lwl_value, disp_value):
    cb=np.float(disp_value)/np.float(lwl_value)/np.float(tc_value)/np.float(bwl)
    if cb > 0.4 or cb < 0.3:
        return dbc.Row([dbc.Col('1) Block Coefficient: {}'.format(round(cb,2)), width=5), dbc.Col('Limits: [0.3-0.4]'), dbc.Col(dbc.Alert("Out of limits", color="danger", style={'padding': '2px', 'display': 'inline-block'}))])
    else:
        return dbc.Row([dbc.Col('1) Block Coefficient: {}'.format(round(cb,2)), width=5), dbc.Col('Limits: [0.3-0.4]'), dbc.Col(dbc.Alert("Within limits", color="success", style={'padding': '2px', 'display': 'inline-block'}))])

@app.callback(
     Output('output-cwp', 'children'),
    [ Input('awp', 'value'), Input('lwl', 'value'), Input('bwl', 'value')])
def callback_bwl(awp, lwl, bwl):
    cwp=np.float(awp)/(np.float(lwl)*np.float(bwl))
    if cwp > 0.71 or cwp < 0.68:
        return dbc.Row([dbc.Col('2) Waterplane Coefficient: {}'.format(round(cwp,2)), width=5), dbc.Col('Limits: [0.68-0.71]'), dbc.Col(dbc.Alert("Out of limits", color="danger", style={'padding': '2px', 'display': 'inline-block'}))])
    else:
        return dbc.Row([dbc.Col('2) Waterplane Coefficient: {}'.format(round(cwp,2)), width=5), dbc.Col('Limits: [0.68-0.71]'), dbc.Col(dbc.Alert("Within limits", color="success", style={'padding': '2px', 'display': 'inline-block'}))])

@app.callback(
    Output('output-conc', 'children'),
    [ Input('awp', 'value')])
def callback_bwl(awp_value):
    sac_obj = codecs.open('data/sacsolution.json', 'r', encoding='utf-8').read()
    sac_solution = json.loads(sac_obj)
    sn_sections = np.asarray(sac_solution["sn_sections"])
    wl_obj = codecs.open('data/wlsolution.json', 'r', encoding='utf-8').read()
    wl_solution = json.loads(wl_obj)
    bn_sections = np.asarray(wl_solution["bn_sections"])
    y_i_wl = np.asarray(wl_solution["y_i_wl"])
    keel_obj = codecs.open('data/keelsolution.json', 'r', encoding='utf-8').read()
    keel_solution = json.loads(keel_obj)
    tn_sections = np.asarray(keel_solution["tn_sections"])
    convex_count=0
    for i in range (0, 10):
        if (bn_sections[i]*tn_sections[i]/2) <= sn_sections[i]:
            convex_count=convex_count+1
    if convex_count==10:
        return dbc.Row([dbc.Col('3) Convexity of sections: {}/10'.format(convex_count), width=5), dbc.Col(''), dbc.Col(dbc.Alert("Convex hull", color="success", style={'padding': '2px', 'display': 'inline-block'}))])
    else:
        return dbc.Row([dbc.Col('3) Convexity of sections: {}/10'.format(convex_count), width=5), dbc.Col(''), dbc.Col(dbc.Alert("Concave hull", color="danger", style={'padding': '2px', 'display': 'inline-block'}))])

@app.callback(
     Output('output-feasibility', 'children'),
    [Input('awp', 'value'), Input('bwl', 'value'), Input('lwl', 'value'), Input('disp', 'value'), Input('tc', 'value')])
def callback_feasibility(awp, bwl, lwl, disp, tc):
    sacmax=np.float(bwl)*np.float(tc)*0.7
    cwp=np.float(awp)/(np.float(lwl)*np.float(bwl))
    cb=np.float(disp)/np.float(lwl)/np.float(tc)/np.float(bwl)
    midship=np.float(sacmax)/(np.float(tc)*np.float(bwl))
    prismatic=np.float(disp)/(np.float(sacmax)*np.float(lwl))
    loadingfactor=np.float(awp)/np.float(disp)**(2/3)
    lwldisp=(np.float(lwl))/np.float(disp)**(1/3)
    bwltc=np.float(bwl)/np.float(tc)
    lwlbwl=np.float(lwl)/np.float(bwl)
    if cwp > 0.71 or cwp < 0.68 or cb > 0.4 or cb < 0.3 or midship > 0.78 or midship < 0.65 or prismatic > 0.6 or prismatic < 0.52 or lwlbwl > 5 or lwlbwl < 2.73 or bwltc > 19.38 or bwltc < 2.46 or lwldisp > 8.5 or lwldisp < 4.34 or loadingfactor > 12.67 or loadingfactor < 3.78:
        return dbc.Alert("The study sailboat may not be feasible. Consider changing its dimensions.", color="danger", style={'width': '80%'}),
    else:
        return dbc.Alert("The study sailboat is feasible. You can proceed.", color="success"),

@app.callback(
    Output('output-submit-dimensions', 'children'),
    [Input('export-dimensions', 'n_clicks'), Input('output-bwlsac', 'children')],
    [State('boat-category', 'value'), State('loa', 'value'), State('lwl','value'), State('disp', 'value'), State('awp', 'value'), State('lcf', 'value'), State('lcb', 'value'), State('beamtransom', 'value'), State('tc', 'value'), State('alpha_f_sac', 'value'), State('alpha_i_sac', 'value'), State('beta_n', 'value')])
def update_output(n_clicks, bwlsac, boatcategory,loa,lwl,disp, awp, lcf, lcb, beamtransom, tc, alpha_f_sac, alpha_i_sac, beta_n):
    sac_obj = codecs.open('data/sacsolution.json', 'r', encoding='utf-8').read()
    sac_solution = json.loads(sac_obj)
    sn_sections = np.asarray(sac_solution["sn_sections"])
    wl_obj = codecs.open('data/wlsolution.json', 'r', encoding='utf-8').read()
    wl_solution = json.loads(wl_obj)
    bn_sections = np.asarray(wl_solution["bn_sections"])
    bwl = np.asarray(wl_solution["bwlmax"])
    y_i_wl = np.asarray(wl_solution["y_i_wl"])
    x_i_wl = np.asarray(wl_solution["x_i_wl"])
    keel_obj = codecs.open('data/keelsolution.json', 'r', encoding='utf-8').read()
    keel_solution = json.loads(keel_obj)
    tn_sections = np.asarray(keel_solution["tn_sections"])
    y_i_keel = np.asarray(keel_solution["y_i_keel"])
    x_i_keel = np.asarray(keel_solution["x_i_keel"])

    section_solution=section_solve(tn_sections, bn_sections, sn_sections, np.float(lwl), np.float(beta_n))
    section_y_sections=section_solution[1]
    section_z_sections=section_solution[2]

    cwp=np.float(awp)/(np.float(lwl)*np.float(bwlsac[0])*2)
    cb=np.float(disp)/np.float(lwl)/np.float(tc)/np.float(bwlsac[0])/2
    cm=np.float(bwlsac[1])/(np.float(tc)*np.float(bwlsac[1])*2)
    cp=np.float(disp)/(np.float(bwlsac[1])*np.float(lwl))
    bwl=np.float(bwlsac[0]*2)

    scb_tot = 0        # lateral area of canoe body
    for z in range(0, 10):
        for i in range (1, 10):
            scb_parc = np.sqrt((section_y_sections[z][i]-section_y_sections[z][i-1])**2+(section_z_sections[z][i]-section_z_sections[z][i-1])**2)
            scb_tot = scb_tot+scb_parc
    scb = np.float(scb_tot)/np.float(10)*np.float(lwl)*2*2.2
    alcb = -simps(y_i_keel, x_i_keel)
    am = 0             # mid-section area
    am = simps(section_y_sections[4], section_z_sections[4])

    sum=0
    for i in range (1,(len(y_i_wl)-1)):
        if (i%2)==0:
            sum=sum+y_i_wl[i]**3*2
        else:
            sum=sum+y_i_wl[i]**3*4
    itwp=2/3*(np.float(sum)/3*np.float(lwl)/100)
    sum=0
    for i in range (1,(len(y_i_wl)-1)):
        if (i%2)==0:
            sum=sum+2*y_i_wl[i]*x_i_wl[i]**2
        else:
            sum=sum+4*y_i_wl[i]*x_i_wl[i]**2
    itwplong=2/3*np.float(sum)*(np.float(lwl)/len(y_i_wl))-np.float(awp)*np.float(lcf)**2
    bmlong = itwplong/np.float(disp)
    #itwp = cwp**2/11.7*lwl*bwl**3   # transversal inertia moment
    bmt = itwp/np.float(disp)
    kb = np.float(tc)*(5/6-cb/(3*cwp))
    kg = 0.1
    gmt = kb+bmt-kg
    gmlong = kb+bmlong-kg

    json.dump({'alcb': alcb, 'category': boatcategory, 'loa': loa, 'lwl': lwl, 'disp': disp, 'awp': awp, 'lcf': lcf, 'lcb': lcb, 'beamtransom': beamtransom, 'tc': tc, 'alpha_f_sac': alpha_f_sac, 'alpha_i_sac': alpha_i_sac, 'beta_n': beta_n, 'cwp': cwp, 'cb': cb, 'cm': cm, 'cp': cp, 'bwl': bwl, 'scb': scb, 'am': am, 'itwp': itwp, 'bmt': bmt, 'kb': kb, 'kg': kg, 'gmt': gmt, 'gmlong': gmlong}, codecs.open('data/dimensions.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)
    
    return 'Data ready.'

@app.callback(Output('output-primary', 'children'), [Input('boat-category', 'value'), Input('loa', 'value')])
def callback_primary(boatcategory, loa):
    if boatcategory == 'cruiser':
        lwl = loa*0.3048*0.90
        bwl = lwl/3.219
        tc = bwl/4.324
        disp = (loa*17-250)*0.0283168
        #disp = (lwl/4.85)**3
        awp = disp**(2/3)*4.996
        lcb = (50-3.29)/100*lwl
        lcf = (50-6.25)/100*lwl
        if loa < 26:
            awp = awp/5
    if boatcategory == 'racer':
        lwl = loa*0.3048*0.95
        bwl = lwl/3.155
        tc = bwl/3.992
        #disp = (lwl/4.775)**3
        disp = (loa*15-225)*0.0283168
        awp = disp**(2/3)*4.976
        lcb = (50-2.29)/100*lwl
        lcf = (50-3.33)/100*lwl
        if loa < 26:
            awp = awp/5
    return html.Details([
            html.Summary('Primary Parameters'),
            html.Br(),
            html.Div([
            dbc.Label("Length Waterline [m]"),
            dbc.Input(type="text", id='lwl', bs_size="sm", value="{}".format(round(lwl,2))),

            dbc.Label("Beam Waterline [m]"),
            dbc.Input(type="text", id='bwl', bs_size="sm", value="{}".format(round(bwl,2))),

            dbc.Label("Draft canoe body [m]"),
            dbc.Input(type='text', id='tc', bs_size="sm", value="{}".format(round(tc,2))),
            html.Div(id='output-tc', className="limits"),

            dbc.Label("Displacement [m3]"),
            dbc.Input(type="text", id="disp", bs_size="sm", value="{}".format(round(disp,2))),
            html.Div(id='output-disp', className="limits"),
            
            dbc.Label("Area Water Plane [m2]"),
            dbc.Input(type='text', id='awp', bs_size="sm", value="{}".format(round(awp,2))),
            html.Div(id='output-awp', className="limits"),

            dbc.Label("LCB [m]"),
            dbc.Input(type='text', id='lcb', bs_size="sm", value="{}".format(round(lcb,2))),
            html.Div(id='output-lcb', className="limits"),

            dbc.Label("LCF [m]"),
            dbc.Input(type='text', id='lcf', bs_size="sm", value="{}".format(round(lcf,2))),
            html.Div(id='output-lcf', className="limits"),

            dbc.Label("Beam at transom [m]"),
            dbc.Input(type='text', id='beamtransom', bs_size="sm", value='0'),
            html.Br(),
            ], className="regularfont"),
    ])

@app.callback(Output('output-secondary', 'children'), [Input('boat-category', 'value'), Input('loa', 'value')])
def callback_secondary(boatcategory, loa):
    if boatcategory == "cruiser": # Sysser 44
        angforesac = 5
        angrearsac = 25
        betan = 0
        cm=0.72
        if loa > 40:
            angforesac = 5
            angrearsac = 40
            cm = 0.8
    if boatcategory == "racer": #Sysse 1
        angforesac = 5
        angrearsac = 25
        betan = 10
        cm=0.65
        if loa > 40:
            angforesac = 5
            angrearsac = 40
            cm = 0.7
    return html.Details([
                html.Summary('Secondary Parameters'),
                html.Div([
                html.Br(),
                dbc.Label("Midsection Coefficient"),
                dbc.Input(type='text', id='cm', bs_size="sm", value="{}".format(round(cm,2))),

                dbc.Label("Fore SAC [degree]"),
                dbc.Input(type='text', id='alpha_f_sac', bs_size="sm", value="{}".format(round(angforesac,2))),

                dbc.Label("Rear SAC [degree]"),
                dbc.Input(type='text', id='alpha_i_sac', bs_size="sm", value="{}".format(round(angrearsac,2))),
                
                dbc.Label("Hull bottom angle [degree]"),
                dbc.Input(type='text', id='beta_n', bs_size="sm", value="{}".format(round(betan,2))),
                ], className="regularfont")
            ]),
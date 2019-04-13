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
import pandas as pd

@app.callback(Output('save-new-dim', 'figure'),
    [Input('tc-new', 'value'), Input('lwl-new', 'value'), Input('disp-new', 'value'), Input('bwl-new', 'value'), Input('lcb-new', 'value'), Input('lcf-new', 'value'), Input('sailset', 'value')])
def create(tcnew, lwlnew, dispnew, bwlnew, lcbnew, lcfnew, sailset):
    json.dump({'tc': tcnew, 'lwl': lwlnew, 'bwl': bwlnew, 'disp': dispnew, 'lcb': lcbnew, 'lcf': lcfnew, 'sailset': sailset}, codecs.open('assets/data/dimensions-basic.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)
    return "ok"

@app.callback(Output('plot-appendages', 'figure'),
    [Input('overhang', 'value'), Input('bowangle', 'value'), Input('freeboard', 'value'), Input('pos-keel', 'value'), Input('sweep-keel', 'value'), Input('span-keel', 'value'), Input('tipchord-keel', 'value'), Input('rootchord-keel', 'value'), Input('heightsurface-rudder', 'value'), Input('span-rudder', 'value'), Input('rootchord-rudder', 'value'), Input('tipchord-rudder', 'value'), Input('sweep-rudder', 'value'), Input('pos-rudder', 'value'), Input('mast-diameter', 'value'), Input('mast-height', 'value'), Input('boom-height', 'value'), Input('psail', 'value'), Input('esail', 'value'), Input('isail', 'value'), Input('jsail', 'value'), Input('mastpos', 'value'), Input('boa', 'value'), Input('rootchord-keel-tcks', 'value'), Input('tipchord-keel-tcks', 'value'), Input('rootchord-rudder-tcks', 'value'), Input('tipchord-rudder-tcks', 'value'), Input('mzn-check', 'value'), Input('pmz', 'value'), Input('emz', 'value'), Input('badmz', 'value'), Input('spl', 'value'), Input('lpg', 'value'), Input('crewmass', 'value'), Input('keel-naca', 'value'), Input('rudder-naca', 'value')])
def create(overhang, bowangle, freeboard, poskeel, sweepkeel, spankeel, tipchordkeel, rootchordkeel, heightsurfacerudder, spanrudder, rootchordrudder, tipchordrudder, sweeprudder, posrudder, mastdiameter, mastheight, boomheight, psail, esail, isail, jsail, mastpos, boa, rootchordkeeltcks, tipchordkeeltcks, rootchordruddertcks, tipchordruddertcks, mzncheck, pmz, emz, badmz, spl, lpg, crewmass, keelnaca, ruddernaca):
    dimensionsobj = codecs.open('assets/data/dimensions-basic.json', 'r', encoding='utf-8').read()
    dimensions = json.loads(dimensionsobj)
    for item in dimensions:
        item = str(item)
        globals()[item] = np.float(dimensions[item])
    overhang = np.float(overhang)
    bowangle = np.radians(np.float(bowangle))
    freeboard = np.float(freeboard)
    poskeel = np.float(poskeel)
    sweepkeel = np.radians(np.float(sweepkeel))
    spankeel = np.float(spankeel)
    tipchordkeel = np.float(tipchordkeel)
    rootchordkeel = np.float(rootchordkeel)
    heightsurfacerudder = np.float(heightsurfacerudder)
    spanrudder = np.float(spanrudder)
    rootchordrudder = np.float(rootchordrudder)
    tipchordrudder = np.float(tipchordrudder)
    sweeprudderdeg = np.float(sweeprudder)
    sweeprudder = np.radians(np.float(sweeprudder))
    posrudder = np.float(posrudder)
    mastdiameter = np.float(mastdiameter)
    boomheight = np.float(boomheight)
    boa = np.float(boa)
    psail = np.float(psail)
    esail = np.float(esail)
    isail = np.float(isail)
    jsail = np.float(jsail)
    mastpos = np.float(mastpos)
    rootchordkeeltcks = np.float(rootchordkeeltcks)
    tipchordkeeltcks = np.float(tipchordkeeltcks)
    rootchordruddertcks = np.float(rootchordruddertcks)
    tipchordruddertcks = np.float(tipchordruddertcks)
    pmz = np.float(pmz)
    emz = np.float(emz)
    badmz = np.float(badmz)
    mzncheck = np.float(mzncheck)

    deckx1 = -overhang
    decky1 = overhang*(tc/(lwl/5))
    deckx2 = deckx1*0.9
    decky2 = freeboard*0.6
    deckx3 = 0
    decky3 = freeboard*0.9
    deckx4 = (np.tan(bowangle)*freeboard)+lwl
    decky4 = freeboard*1.1
    deckx5 = lwl
    decky5 = 0
    cockpitx1 = lwl*0.3
    cockpity1 = freeboard*(0.9+0.2*cockpitx1/deckx4)
    cockpitx2 = lwl*0.35
    cockpity2 = freeboard*1.3
    cockpitx3 = lwl*0.65
    cockpity3 = freeboard*1.3
    cockpitx4 = lwl*0.8
    cockpity4 = freeboard*(0.9+0.2*cockpitx4/deckx4)
    keelx1 = poskeel+rootchordkeel/2
    keely1 = 0
    keelx2 = keelx1-np.tan(sweepkeel)*spankeel
    keely2 = -tc-spankeel
    keelx3 = keelx2-tipchordkeel
    keely3 = -tc-spankeel
    keelx4 = keelx1-rootchordkeel
    keely4 = 0
    rudderx1 = posrudder+rootchordrudder/2
    ruddery1 = heightsurfacerudder
    rudderx2 = rudderx1-np.tan(sweeprudder)*spanrudder
    ruddery2 = -spanrudder+heightsurfacerudder
    rudderx3 = rudderx2-tipchordrudder
    ruddery3 = -spanrudder+heightsurfacerudder
    rudderx4 = rudderx1-rootchordrudder
    ruddery4 = heightsurfacerudder
    mastdeflection=0.15
    mastx1 = mastpos
    masty1 = freeboard*1.3
    mastx2 = mastpos+mastdiameter
    masty2 = freeboard*1.3
    mastx3 = mastpos+mastdiameter-mastdeflection
    masty3 = freeboard*1.3+boomheight+psail
    mastx4 = mastpos-mastdeflection
    masty4 = freeboard*1.3+boomheight+psail
    boomx1 = mastpos
    boomy1 = freeboard+boomheight-mastdiameter/2
    boomx2 = mastpos-esail
    boomy2 = freeboard+boomheight-mastdiameter/2
    boomx3 = mastpos-esail
    boomy3 = freeboard+boomheight+mastdiameter/2
    boomx4 = mastpos
    boomy4 = freeboard+boomheight+mastdiameter/2
    jibx1 = deckx4
    jiby1 = decky4
    jibx2 = deckx4-jsail
    jiby2 = freeboard+boomheight*0.5
    jibx3 = mastpos-mastdiameter/2
    jiby3 = freeboard+isail
    #centre of effort
    arearudder = spanrudder*(rootchordrudder+tipchordkeel)/2
    areakeel = spankeel*(rootchordkeel+tipchordkeel)/2
    areahull = lwl*tc*0.7
    b=rootchordkeel
    a=tipchordkeel
    cekeely = spankeel/3*((2*a+b)/(a+b))
    cekeelx = -(poskeel-(keelx2+keelx3)/2)/spankeel*cekeely
    d=rootchordkeel
    c=tipchordkeel
    ceruddery = spanrudder/3*((2*c+d)/(c+d))
    cerudderx = -(posrudder-(rudderx2+rudderx3)/2)/spanrudder*ceruddery
    cehidrox = ((cekeelx+poskeel)*areakeel+(cerudderx+posrudder)*arearudder+lwl/2*(areahull))/(areakeel+arearudder+areahull)
    cehidroy = (-(cekeely+tc)*areakeel-(ceruddery+heightsurfacerudder)*arearudder-tc*0.25*(areahull))/(areakeel+arearudder+areahull)
    lr = cehidrox-cerudderx

    mainarea = psail*esail/2
    if sailset == 1 or sailset == 3:
        jibarea = isail*jsail/2
        area = mainarea+jibarea
        cesailx = (mainarea*(-esail/3+mastpos)+jibarea*(deckx4-jsail*2/3))/(area)
        cesaily = (mainarea*(psail/3+boomheight+freeboard)+jibarea*(decky4+jsail/3))/(area)
    if sailset == 2 or sailset == 4:
        cesailx = (-esail/3+mastpos)
        cesaily = (psail/3+boomheight+freeboard)

    spl = np.float(spl)
    lpg = np.float(lpg)
    mastheight = np.float(mastheight)+psail
    xcea = cesailx/lwl
    marcaR = np.float(ruddernaca)
    marcaK = np.float(keelnaca)

    json.dump({'p': psail, 'e': esail, 'i': isail, 'j': jsail, 'bad': boomheight, 'spl': spl, 'lpg': lpg, 'pmz': pmz, 'emz': emz, 'badmz': badmz, 'boa': boa, 'fb': freeboard, 'lr': lr, 'ehm': mastheight, 'emdc': mastdiameter, 'spanR': spanrudder, 'tipcR': tipchordrudder, 'rootcR': rootchordrudder, 'tiptcksR': tipchordruddertcks, 'roottcksR': rootchordruddertcks, 'sweepRdeg': sweeprudderdeg, 'spanK': spankeel, 'tipcK': tipchordkeel, 'rootcK': rootchordkeel, 'tiptcksK': tipchordkeeltcks, 'roottcksK': rootchordkeeltcks, 'sweepKdeg': sweepkeel, 'xcea': xcea, 'mcrew': crewmass, 'marcaR': marcaR, 'marcaK': marcaK, 'hsr': heightsurfacerudder}, codecs.open('assets/data/dimensions-appendages.json', 'w', encoding='utf-8'), separators=(', ',': '), sort_keys=True)

    return {
        'data': [
            go.Scatter(
                x=[lcf],
                y=[0],
                text=['LCF'],
                name='LCF',
                cliponaxis=False,
            ),
            go.Scatter(
                x=[lcb],
                y=[0],
                text=['LCB'],
                name='LCB',
                cliponaxis=False,
            ),
            go.Scatter(
                x=[cekeelx+poskeel],
                y=[-cekeely-tc],
                text=['CE Keel'],
                name='CE Keel',
                cliponaxis=False,
            ),
            go.Scatter(
                x=[cerudderx+posrudder],
                y=[-ceruddery-heightsurfacerudder],
                text=['CE Rudder'],
                name='CE Rudder',
                cliponaxis=False,
            ),
            go.Scatter(
                x=[cesailx],
                y=[cesaily],
                text=['CE Aero'],
                name='CE Aero',
                cliponaxis=False,
            ),
            go.Scatter(
                x=[cehidrox],
                y=[cehidroy],
                text=['CE Hydro'],
                name='CE Hydro',
                cliponaxis=False,
            ),
        ],
        'layout': go.Layout(
            height=800,
            xaxis= {
                'range': [deckx1*1.1-emz, deckx5*1.1+2+boa],
                'zeroline': False,
                'title': "Length [m]",
                'dtick': 1, 
            },
            yaxis= {
                'range': [keely3*1.5, masty4*1.1],
                'showgrid': False,
                'title': "Height [m]",
                'scaleanchor':"x",
                'scaleratio': 1,
            },
            margin = {
                "r": 30,
                "t": 30,
                "b": 30,
                "l": 30
            },
            shapes= [
            {#deckcurve
                'type': 'path',
                'path': ' M 0,0 L{},{} L{},{} L{},{}, L{},{} L{},{} Z'.format(deckx1, decky1, deckx2, decky2, deckx3, decky3, deckx4, decky4, deckx5, decky5),
                'layer': 'above',
                'line': {'width': 1},
            },
            {#cockpit
                'type': 'path',
                'path': ' M {},{} L {},{} L {},{} L {},{}'.format(cockpitx1, cockpity1, cockpitx2, cockpity2, cockpitx3, cockpity3, cockpitx4, cockpity4),
                'layer': 'above',
                'line': {'width': 1},
            },
            {#keel
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(keelx1, keely1, keelx2, keely2, keelx3, keely3, keelx4, keely4),
                'layer': 'below',
                'line': {'width': 1},
            },
            {#rudder
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(rudderx1, ruddery1, rudderx2, ruddery2, rudderx3, ruddery3, rudderx4, ruddery4),
                'layer': 'below',
                'line': {'width': 1},
            },
            {#keel curve
                'type': 'path',
                'path': 'M 0,0 C {},{} {},{} {},0'.format(lwl/3, -tc*1.35, 2*lwl/3, -tc*1.35, lwl),
                'line': {'color': 'black'},
                'fillcolor': 'white',
                'layer': 'below',
                'line': {'width': 1},
            },
            {#boom
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(boomx1, boomy1, boomx2-mastdiameter, boomy2, boomx3-mastdiameter, boomy3, boomx4, boomy4),
                'layer': 'below',
                'fillcolor': 'white',
                'line': {'width': 1},
            },
            {#mast
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(mastx1, masty1, mastx2, masty2, mastx3, masty3, mastx4, masty4),
                'layer': 'above',
                'fillcolor': 'white',
                'line': {'width': 1},
            },
            {#main sail
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} Z'.format(boomx4, boomy4, boomx3, boomy3, mastx4, masty4),
                'layer': 'below',
                'fillcolor': 'rgba(255, 140, 184, 0.1)',
                'line': {'width': 1},
            },
            {#jib sail
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} Z'.format(jibx1, jiby1, jibx2, jiby2, jibx3, jiby3) if sailset == 1 or sailset == 3 else '',
                'layer': 'below',
                'fillcolor': 'rgba(93, 164, 214, 0.1)',
                'line': {'width': 1},
            },
            {#spinnaker sail #1
                'type': 'path',
                'path': 'M {},{} Q {},{} {},{}'.format(lwl*0.65, freeboard+psail/8,lwl*0.85, freeboard+psail*0.15, deckx4, decky4) if sailset == 2 or sailset == 3 else '',
                'layer': 'below',
                'line': {'width': 1},
            },
            {#spinnaker sail #2
                'type': 'path',
                'path': 'M {},{} Q {},{} {},{}'.format(lwl*0.65, freeboard+psail/8,lwl*0.8, freeboard+psail/2, mastpos,freeboard+psail*0.9) if sailset == 2 or sailset == 3 else '',
                'layer': 'below',
                'line': {'width': 1},
            },
            {#spinnaker sail #3
                'type': 'path',
                'path': 'M {},{} Q {},{} {},{}'.format(mastpos, freeboard+psail*0.9,deckx4*1.1, freeboard+psail*0.8, deckx4, decky4) if sailset == 2 or sailset == 3 else '',
                'layer': 'below',
                'line': {'width': 1},
            },
            {#spinnaker line
            'type': 'line',
                'x0': lwl*0.65 if sailset == 2 or sailset == 3 else '',
                'y0': freeboard+psail/8 if sailset == 2 or sailset == 3 else '',
                'x1': deckx3 if sailset == 2 or sailset == 3 else '',
                'y1': decky3 if sailset == 2 or sailset == 3 else '',
                'layer': 'below',
                'line': {'width': 1, 'color': 'grey'},
            },
            {#main line
            'type': 'line',
                'x0': deckx3,
                'y0': decky3,
                'x1': boomx2,
                'y1': boomy2,
                'layer': 'below',
                'line': {'width': 1, 'color': 'grey'},
            },
            {#jib line
            'type': 'line',
                'x0': cockpitx1,
                'y0': cockpity1,
                'x1': jibx2,
                'y1': jiby2,
                'layer': 'below',
                'line': {'width': 1, 'color': 'grey'},
            },
            {#keel profile
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(deckx4+1+boa/2-rootchordkeel*rootchordkeeltcks/2, 0, deckx4+1+boa/2+rootchordkeel*rootchordkeeltcks/2, 0, deckx4+1+boa/2+tipchordkeel*tipchordkeeltcks/2, -tc-spankeel, deckx4+1+boa/2-tipchordkeel*tipchordkeeltcks/2, -tc-spankeel),
                'layer': 'below',
                'line': {'width': 1},
            },
            {#rudder profile
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(deckx4+1+boa/2-rootchordrudder*rootchordruddertcks/2, 0, deckx4+1+boa/2+rootchordrudder*rootchordruddertcks/2, 0, deckx4+1+boa/2+tipchordrudder*tipchordruddertcks/2, -heightsurfacerudder-spanrudder, deckx4+1+boa/2-tipchordrudder*tipchordruddertcks/2, -heightsurfacerudder-spanrudder),
                'layer': 'below',
                'line': {'width': 1},
            },
            #{#mast profile
            #    'type': 'path',
            #    'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(deckx4+1+boa*0.5-mastdiameter/2, 0, deckx4+1+boa*0.5+mastdiameter/2, 0, deckx4+1+boa*0.5+mastdiameter/2, masty3, deckx4+1+boa*0.5-mastdiameter/2, masty3),
            #    'layer': 'below',
            #    'fillcolor': 'white',
            #    'line': {'width': 1},
            #},
            {#deck profile
                'type': 'path',
                'path': 'M {},{} C {},{} {},{} {},{}'.format(deckx4+1, freeboard, deckx4+1+boa*0.05, -1.9*tc, deckx4+1+boa*0.95, -1.9*tc, deckx4+1+boa, freeboard),
                'line': {'width': 1},
                'fillcolor': 'white',
                'layer': 'below',
            },
            {#deck upper profile
                'type': 'path',
                'path': 'M {},{} Q {},{} {},{}'.format(deckx4+1, freeboard, deckx4+1+boa/2, freeboard*1.2, deckx4+1+boa, freeboard),
                'line': {'width': 1},
            },
            {#mizzen mast
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(deckx3, decky3, deckx3+mastdiameter, decky3, deckx3+mastdiameter, decky3+pmz+badmz, deckx3, decky3+pmz+badmz) if mzncheck == 1 else '',
                'layer': 'above',
                'fillcolor': 'white',
                'line': {'width': 1},
            },
            {#mizzen sail
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} Z'.format(deckx3, decky3+badmz, deckx3, decky3+pmz+badmz, deckx3-emz, decky3+badmz) if mzncheck == 1 else '',
                'layer': 'below',
                'fillcolor': 'rgba(255, 140, 184, 0.1)',
                'line': {'width': 1},
            },
            {#boom
                'type': 'path',
                'path': ' M {},{} L{},{} L{},{} L{},{} Z'.format(deckx3, decky3+badmz, deckx3-emz*1.1, decky3+badmz, deckx3-emz*1.1, decky3+badmz-mastdiameter, deckx3, decky3+badmz-mastdiameter) if mzncheck == 1 else '',
                'layer': 'below',
                'fillcolor': 'white',
                'line': {'width': 1},
            },
            {#waterline
            'type': 'line',
                'x0': -100,
                'y0': 0,
                'x1': 100,
                'y1': 0,
                'line': {'width': 1, 'color': 'rgb(78,179,211,0.05)'},
            },
            ],
            font=dict(size=10),
            legend=dict(x=0, y=1),
        )
    }
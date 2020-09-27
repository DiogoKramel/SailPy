import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import json, codecs
import numpy as np
import pandas as pd
import os
#import redis

from app import app
from layouts import introduction, dimensionshull, optimizationhull, resultshulll, dimensionsappendages, optimizationappendages, resultsappendages, saildata

server = app.server

#if "DYNO" in os.environ:
#    if bool(os.getenv("DASH_PATH_ROUTING", 0)):
#        app.config.requests_pathname_prefix = "/{}/".format(os.environ["DASH_APP_NAME"])

#redis_instance = redis.StrictRedis.from_url(os.environ["REDIS_URL"])

# logos and hyperlinks
logoapp = html.Img(src='assets/static/logoappwhite.png', height='50px')
logousp = html.A([
    html.Img(src='assets/static/logousp.png', height='35px')], 
    href='https://www.usp.br', target='_blank')
logopoli = html.A([
    html.Img(src='assets/static/logopolitecnica.png', height='35px')], 
    href='https://www.poli.usp.br/', target='_blank')
logopnv = html.A([
    html.Img(src='assets/static/logopnv.png', height='35px')], 
    href='https://www.pnv.poli.usp.br/', target='_blank')
logocapes = html.A([
    html.Img(src='assets/static/logocapes.png', height='35px')], 
    href='https://www.capes.gov.br', target='_blank')
logogit = html.A([
    html.Img(src='assets/static/logogithub.svg', height='35px')], 
    href='https://github.com/DiogoKramel/SailPy', target='_blank')

# landing page
landpage = html.Div([
    dbc.Row(dbc.Col(logoapp, width='auto', style={'padding-top': '10pt', 'padding-left':'20pt'})),
    dbc.Row([
        dbc.Jumbotron([
            html.H3('SailPy', className='display-3'),
            html.P('A preliminary design tool for sailboats', className='lead'),
            html.Hr(className='my-2'),
            html.P("SailPy is an opensource Python application for conceptual sailboat design with an object-oriented approach. The sailboat is simulated in different conditions, to which optimization tools are applied to evaluate its performance, assisting the definition of the best set of dimensions in order to meet the user's needs. This library encourages suggestions, new features, improvements, and report of bugs. The scripts and issues being discussed can be found at the GitHub page linked in the page bottom.", className='justify'),
            html.Hr(className='my-2'),
            html.Br(),
            dbc.Button(dcc.Link(html.Div(html.Div('Start the analysis', className='btnupdate')), href=f'/application', style={'color': 'white'})),
        ], className='landingjumbo'),
    ], className='middle'),
], className='backgroundlanding')

# title at top bar
title = dcc.Link('SailPy - A preliminary design tool for sailboats', href='/', className='navbar-brand', style={'color': 'white'})

# top bar itens
navitems = html.Ul([
    dbc.NavItem(dbc.NavLink('Home', href='/')),
    dbc.DropdownMenu(
        nav=True, 
        in_navbar=True, 
        label='Menu',
        children=[
            dbc.DropdownMenuItem('About'),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem('Authors'),
            dbc.DropdownMenuItem('Contact'),
        ],
    ),
], className = 'navbar-nav')

# top bar
topbar = html.Nav([
    dbc.Container([
        dbc.Row([
            dbc.Col(logoapp, width='auto'),
            dbc.Col(title, width='auto'),
            dbc.Col(navitems, width='auto'),
        ], justify='between', align='center', style={'width': '100%'}),
    ]),
], className='navbar navbar-expand-lg navbar-dark bg-dark') # bg-dark or bg-primary

# navigation tabs
tabs = html.Div([
    dcc.Tabs(id='tabs-styled-with-inline', value='tab-1', children=[
        dcc.Tab(label='Introduction', value='tab-1'),
        dcc.Tab(label='Hull Dimensions', value='tab-2'),
        dcc.Tab(label='Optimization', value='tab-3'),
        dcc.Tab(label='Optimization Results', value='tab-4'),
        dcc.Tab(label='Appendages, Sail and Polar diagram', value='tab-5'),
        #dcc.Tab(label='Optimization II', value='tab-6'),
        #dcc.Tab(label='Results II', value='tab-7'),
    ], style={'height': '30pt', 'font-size': '11pt', 'line-height': '11pt', 'margin-bottom': '5pt'}),
])

# bottom 
footer = html.Nav([
    dbc.Container([
        dbc.Row([
            dbc.Col(logousp, width='auto'),
            dbc.Col(logopoli, width='auto'),
            dbc.Col(logopnv, width='auto'),
            dbc.Col(logocapes, width='auto'),
            dbc.Col([
                html.P('Source code released under the', style={'display': 'inline-block', 'margin-right': '3px'}),
                html.A('MIT license', href='https://opensource.org/licenses/MIT/', target='_blank', style={'display': 'inline-block'}),
                html.P('. Website and documentation licensed under', style={'display': 'inline-block', 'margin-right': '3px'}), 
                html.A('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/', target='_blank', style={'display': 'inline-block'}),
            ], style={'display': 'inline-block', 'margin-top': '5px'}),
            dbc.Col(logogit, width='auto'),
        ]),
    ]),
], className='navbar footer footerbottom')

# title in tab browser
app.title = 'SailPy'

# meta data and favicon
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Meta(name='viewport', 
        content='width=device-width, initial-scale=1.0',
        title='SailPy - Developed by Diogo Kramel in 2019'),
    html.Link(href='/assets/static/favicon.ico'),
    html.Div(id='landing-application'),
])

# pages called when moving between tabs
@app.callback(Output('page-content', 'children'), [Input('tabs-styled-with-inline', 'value')])
def display_page(tab):
    space = html.Div([html.Br(), html.Br(), html.Br(), html.Br(), html.Br()])
    if tab == 'tab-1':
        return html.Br(), introduction.introduction, space, footer
    elif tab == 'tab-2':
        return html.Br(), dimensionshull.hull, space, footer
    elif tab == 'tab-3':
        return html.Br(), optimizationhull.optimizationhull, space, footer
    elif tab == 'tab-4':
        datatable = pd.read_csv("assets/data/optimizationresistance.csv")
        datatable = datatable.loc[datatable['valid']==True]
        datatable = datatable.loc[:,"id":"LCB"]
        return html.Br(), resultshulll.resultshull, space, footer
    elif tab == 'tab-5':
        return html.Br(), dimensionsappendages.appendages, space, footer
    #elif tab == 'tab-6':
        #return html.Br(), optimizationappendages.optimizationappendages, space, footer
    elif tab == 'tab-7':
        return html.Br(), resultsappendages.resultsappendages, space, footer
    else:
        return ''

# a different callback for the landing page due to layout differences
@app.callback(Output('landing-application', 'children'), [Input('url', 'pathname')])
def display_landing(pathname):
    space = html.Div([html.Br(), html.Br(), html.Br(), html.Br(), html.Br()])
    if pathname == '/':
        return landpage, footer
    elif pathname == '/application':
        return topbar, tabs, html.Div(id='page-content')
    elif pathname == '/saildata':
        return topbar, saildata.saildata, space, footer
    else:
        return '404'

# importing external css to add and configure the icons used
external_css = ['https://use.fontawesome.com/releases/v5.7.2/css/all.css', 'assets/fonts/et-line-font/style.css']
for css in external_css:
    app.css.append_css({'external_url': css})

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))

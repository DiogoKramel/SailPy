import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table_experiments import DataTable
import plotly.graph_objs as go
import json, codecs
import numpy as np

from app import app
from layouts import introduction, dimensionshull, optimizationhull, resultshulll, dimensionsappendages, optimizationappendages, resultsappendages, saildata

server = app.server

logoapp = html.Img(src='/assets/static/logoapp.png', height='45px')
logoappwhite = html.Img(src='/assets/landing/logoappwhite.png', height='50px')
logousp = html.A([html.Img(src='/assets/static/logousp.png', height='35px')], href="https://www.usp.br/")
logopoli = html.A([html.Img(src='/assets/static/logopolitecnica.png', height='35px')], href="https://www.poli.usp.br/")
logopnv = html.A([html.Img(src='/assets/static/pnv.png', height='35px')], href="www.pnv.poli.usp.br/")
logocapes = html.A([html.Img(src='/assets/static/logocapes.png', height='35px')], href="http://www.capes.gov.br")
logogit = html.A([html.Img(src='/assets/static/github.svg', height='35px')], href="https://github.com/DiogoKramel/SailPy")
title = dcc.Link('SailPy - A preliminary design tool for sailboats', className='navbar-brand', style={'color': 'white'})

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
], className = "navbar-nav")

navbar = html.Nav([
    dbc.Container([
        dbc.Row([
            dbc.Col(logoappwhite, width='auto'),
            dbc.Col(title, width='auto'),
            dbc.Col(navitems, width='auto'),
        ], justify='between', align='center', style={'width': '100%'}),
    ]),
], className='navbar navbar-expand-lg navbar-dark bg-dark')		# bg-dark or bg-primary

footer = html.Nav([
    dbc.Container([
        dbc.Row([
            dbc.Col(logousp, width='auto'),
            dbc.Col(logopoli, width='auto'),
            dbc.Col(logopnv, width='auto'),
            dbc.Col(logocapes, width='auto'),
            dbc.Col([
                html.P('Source code released under the', style={'display': 'inline-block', 'margin-right': '3px'}),
                html.A('MIT license', href='https://opensource.org/licenses/MIT/', style={'display': 'inline-block'}),
                html.P('. Website and documentation licensed under', style={'display': 'inline-block', 'margin-right': '3px'}), 
                html.A('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/', style={'display': 'inline-block'}), 
                html.P('.', style={'display': 'inline-block', 'margin-top':'10px'}),
            ], style={'display': 'inline-block'}),
            dbc.Col(logogit, width='auto'),
        ]),
    ]),
], className='navbar footer footerbottom')

landpage = html.Div([
    dbc.Row(dbc.Col(logoappwhite, width='auto', style={'padding-top': '10pt', 'padding-left':'20pt'})),
    dbc.Row([
        dbc.Jumbotron([
            html.H3('SailPy', className='display-3'),
            html.P('A preliminary design tool for sailboats', className='lead'),
            html.Hr(className='my-2'),
            html.P("SailPy is an opensource Python application for conceptual sailboat design with an object-oriented approach. The sailboat is simulated in different conditions, to which optimization tools are applied to evaluate its performance, assisting the definition of the best set of dimensions in order to meet the user's needs. This library encourages suggestions, new features, improvements, and report of bugs. The link to the scripts you can find at the GitHub icon in the page bottom.", className='justify'),
            html.Hr(className='my-2'),
            html.Br(),
            html.P(dbc.Button(dcc.Link(html.Div(html.Div('Start the analysis', className='btnupdate'), className='fa fa-arrow-circle-right btnupdate'), href=f'/application', style={'color': 'white'}))),
        ], className='landingjumbo'),
    ], className='middle'),
], className='backgroundlanding')

tabs = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Introduction', value='tab-1'),
        dcc.Tab(label='Hull Dimensions', value='tab-2'),
        dcc.Tab(label='Optimization I', value='tab-3'),
        dcc.Tab(label='Results I', value='tab-4'),
        dcc.Tab(label='Appendages & Sail', value='tab-5'),
        dcc.Tab(label='Optimization II', value='tab-6'),
        dcc.Tab(label='Results II', value='tab-7'),
    ], style={'height': '30pt', 'font-size': '11pt', 'line-height': '11pt', 'margin-bottom': '5pt'}),
])

app.title = 'SailPy'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Meta(name='viewport', 
        content='width=device-width, initial-scale=1.0',
        title='SailPy. Developed by Diogo Kramel. 2019.'),
    html.Link(href='/assets/static/favicon.ico'),
    html.Div(id='landing-application'),
])

@app.callback(Output('page-content', 'children'), [Input('tabs-styled-with-inline', 'value')])
def display_page(tab):
    space = html.Div([html.Br(), html.Br(), html.Br(), html.Br(), html.Br()])
    if tab == 'tab-1':
        return introduction.introduction, space, footer
    elif tab == 'tab-2':
        return dimensionshull.hull, space, footer
    elif tab == 'tab-3':
        return optimizationhull.optimizationhull, space, footer
    elif tab == 'tab-4':
        return resultshulll.resultshull, resultshulll.resultsplus, space, footer
    elif tab == 'tab-5':
        dim = codecs.open('assets/data/dimensions-hull.json', 'r', encoding='utf-8').read()
        dim = json.loads(dim)
        lwl = np.float(dim["lwl"])
        bwl = np.float(dim["bwl"])
        lcb = np.float(dim["lcb"])
        lcf = np.float(dim["lcf"])
        disp = np.float(dim["disp"])
        tc = np.float(dim["tc"])
        return dimensionsappendages.appendages, space, footer
    elif tab == 'tab-6':
        return optimizationappendages.optimizationappendages, space, footer
    elif tab == 'tab-7':
        return resultsappendages.resultsappendages, space, footer
    else:
        return ''

@app.callback(Output('landing-application', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return landpage, footer
    elif pathname == '/application':
        return navbar, tabs, html.Div(id='page-content')
    elif pathname == '/saildata':
        return navbar, tabs, saildata, footer
    else:
        return '404'


external_css = ['https://use.fontawesome.com/releases/v5.7.2/css/all.css', 'assets/fonts/et-line-font/style.css']
for css in external_css:
    app.css.append_css({'external_url': css})

if __name__ == '__main__':
    app.run_server(debug=True)
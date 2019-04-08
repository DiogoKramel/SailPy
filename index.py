import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table_experiments import DataTable
import plotly.graph_objs as go

from app import app
from layouts import introduction, dimensionshull, optimizationhull, resultshulll, dimensionsappendages

server = app.server

logoapp = html.Img(src = "/assets/static/logoapp.png", height = "60px")
logoappwhite = html.Img(src = "/assets/landing/logoappwhite.png", height = "80px")
logousp = html.Img(src = "/assets/static/logousp.png", height = "35px")
logopoli = html.Img(src = "/assets/static/logopolitecnica.png", height = "35px")
logopnv = html.Img(src = "/assets/static/pnv.png", height = "35px")
logocapes = html.Img(src = "/assets/static/logocapes.png", height = "35px")
title = dcc.Link("A preliminary design tool for sailboats", className = "navbar-brand")

navitems = html.Ul([
    dbc.NavItem(dbc.NavLink("Home", href = "/introduction")),
    dbc.DropdownMenu(
        nav = True, 
        in_navbar = True, 
        label = "Menu",
        children = [
            dbc.DropdownMenuItem("About"),
            dbc.DropdownMenuItem(divider = True),
            dbc.DropdownMenuItem("Authors"),
            dbc.DropdownMenuItem("Contact"),
        ],
    ),
], className = "navbar-nav")

navbar = html.Nav([
    dbc.Container([
        dbc.Row([
            dbc.Col(logoapp, width = "auto"),
            dbc.Col(title, width = "auto"),
            dbc.Col(navitems, width = "auto"),
        ], justify = "between", align = "center", style={"width": "100%"}),
    ]),
], className="navbar navbar-light navbar-expand-md bg-light sticky-top")

stepbar = dbc.Container([
    dbc.Nav([
        dbc.NavItem(dbc.NavLink("Introduction", href="/introduction")),
        dbc.NavItem(dbc.NavLink("Hull", href="/dimensionshull")),
        dbc.NavItem(dbc.NavLink("Optimization", href="/optimizationhull")),
        dbc.NavItem(dbc.NavLink("Results I", href="/resultshull")),
        dbc.NavItem(dbc.NavLink("Dimensions", href="/dimensionsappendages")),
    ], pills=True, justified=True),
], className="stepbarheight")

footer = html.Nav([
    dbc.Container([
        dbc.Row([
            dbc.Col(logousp, width="auto"),
            dbc.Col(logopoli, width="auto"),
            dbc.Col(logopnv, width="auto"),
            dbc.Col(logocapes, width="auto"),
            dbc.Col([
                html.P("Source code released under the", style={ 'display': 'inline-block', 'margin-right': '3px'}),
                dcc.Link('MIT license', href='https://opensource.org/licenses/MIT', style={ 'display': 'inline-block'}),
                html.P(". Website and documentation licensed under", style={ 'display': 'inline-block', 'margin-right': '3px'}), 
                dcc.Link('CC BY 4.0', href='https://creativecommons.org/licenses/by/4.0/', style={ 'display': 'inline-block'}), 
                html.P(".", style={ 'display': 'inline-block', 'margin-top':'10px',}),
            ], style={ 'display': 'inline-block'}),
        ]),
    ]),
], className="navbar footer")

landpage = html.Div([
    dbc.Row(dbc.Col(logoappwhite, width="auto")),
    dbc.Row([
        dbc.Jumbotron([
            html.H3("App Name", className="display-3"),
            html.P("A preliminary design tool for sailboats", className="lead"),
            html.Hr(className="my-2"),
            html.P("Application Name is an opensource Python application for conceptual sailboat design with an object-oriented framework. The vessel is simulated in different conditions, applying optimization tools to evaluate its design, assisting the choice of the best set of dimensions in order to meet the user's needs.", className="justify"), #The library is developed by Ship Design and Operation Lab at Norwegian University of Science and Technology (NTNU) in Ålesund.
            html.Hr(className="my-2"),
            html.Br(),
            html.P(dbc.Button(dcc.Link(html.Div("Start the analysis"), href=f"/introduction", style={'color': 'white'}))),
        ], className='landingjumbo'),
    ], className='middle'),
], className="backgroundlanding")


app.title = 'Application Name'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Meta(name='viewport', 
		content='width=device-width, initial-scale=1.0',
		title='Application Name. Developed by Diogo Kramel. 2019.'),
    html.Link(href='/assets/static/favicon.ico'),
    html.Div(id='page-content'),
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return landpage, footer
    elif pathname == '/introduction':
        return navbar, stepbar, dbc.DropdownMenuItem(divider=True), introduction.introduction, footer
    elif pathname == '/dimensionshull':
        return navbar, stepbar, dbc.DropdownMenuItem(divider=True), dimensionshull.hull, footer
    elif pathname == '/optimizationhull':
        return navbar, stepbar, dbc.DropdownMenuItem(divider=True), optimizationhull.optimizationhull, footer
    elif pathname == '/resultshull':
        return navbar, stepbar, dbc.DropdownMenuItem(divider=True), resultshulll.resultshull, resultshulll.resultsplus, footer
    elif pathname == '/dimensionsappendages':
        return navbar, stepbar, dbc.DropdownMenuItem(divider=True), dimensionsappendages.appendages, footer
    else:
        return '404'


external_css = ["https://use.fontawesome.com/releases/v5.7.2/css/all.css", "assets/fonts/et-line-font/style.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)
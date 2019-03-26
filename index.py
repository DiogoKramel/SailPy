import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_table_experiments import DataTable
import plotly.graph_objs as go

from app import app
from layouts import introduction, dimensionshull, optimizationhull, resultshulll

server = app.server

logoapp = html.Img(src = "/assets/static/logoapp.png", height = "80px")
logousp = html.Img(src = "/assets/static/logousp.png", height = "40px")
logopoli = html.Img(src = "/assets/static/logopolitecnica.png", height = "40px")
logocapes = html.Img(src = "/assets/static/logocapes.png", height = "40px")
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

footer = html.Nav([
    dbc.Container([
        dbc.Row([
            dbc.Col(logousp, width="auto"),
            dbc.Col(logopoli, width="auto"),
            dbc.Col(logocapes, width="auto"),
        ], align="center", style={"width": "100%"}),
    ]),
], className="navbar footer")

stepbar = dbc.Container([
    dbc.Nav([
        dbc.NavItem(dbc.NavLink("Introduction", href="/introduction")),
        dbc.NavItem(dbc.NavLink("Hull", href="/dimensionshull")),
        dbc.NavItem(dbc.NavLink("Optimization", href="/optimizationhull")),
        dbc.NavItem(dbc.NavLink("Results I", href="/resultshull")),
    ], pills=True, justified=True),
], className="mt-4")


app.title = 'Application Name'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Meta(name='viewport', content='width=device-width, initial-scale=1.0',
              title='Application name. Developed by Diogo Kramel. 2019.'),
    html.Link(href='/assets/static/favicon.ico'),
    navbar,
    stepbar,
    dbc.DropdownMenuItem(divider=True),
    html.Div(id='page-content'),
    footer
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return introduction.introduction
    elif pathname == '/introduction':
        return introduction.introduction
    elif pathname == '/dimensionshull':
        return dimensionshull.hull
    elif pathname == '/optimizationhull':
        return optimizationhull.optimizationhull
    elif pathname == '/resultshull':
        return resultshulll.resultshull, resultshulll.resultsplus
    else:
        return '404'


external_css = ["https://use.fontawesome.com/releases/v5.7.2/css/all.css", "assets/fonts/et-line-font/style.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq


logo = html.Img(src="/assets/static/logoapp.png", height="80px")
logocapes = html.Img(src="/assets/static/logocapes.png", height="60px")
logopoli = html.Img(src="/assets/static/logopolitecnica.png", height="60px")
logousp = html.Img(src="/assets/static/logousp.png", height="60px")
title = dcc.Link("A preliminary design tool for sailboat optimization", className="navbar-brand")

navitems = html.Ul([
    dbc.NavItem(dbc.NavLink("Home", href="/introduction")),
    dbc.DropdownMenu(
        nav=True, in_navbar=True, label="Menu",
        children=[
            dbc.DropdownMenuItem("About"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("Authors"),
            dbc.DropdownMenuItem("Contact"),
        ],
    ),
], className="navbar-nav")

navbar = html.Nav([
    dbc.Container([
        dbc.Row([
            dbc.Col(logo, width="auto"),
            dbc.Col(title, width="auto"),
            dbc.Col(navitems, width="auto"),
        ], justify="between", align="center", style={"width": "100%"}),
    ]),
], className="navbar navbar-light navbar-expand-md bg-light sticky-top")

bottombar = html.Nav([
    dbc.Container([
        dbc.Row([
            dbc.Col(logousp, width="auto"),
            dbc.Col(logopoli, width="auto"),
            dbc.Col(logocapes, width="auto"),
        ], align="center", style={"width": "100%"}),
    ]),
], className="navbar")

stepbar = dbc.Container([
    dbc.Nav([
        dbc.NavItem(dbc.NavLink("Introduction", href="/introduction")),
        dbc.NavItem(dbc.NavLink("Hull", href="/hull")),
        dbc.NavItem(dbc.NavLink("Optimization", href="/optimizationhull")),
        dbc.NavItem(dbc.NavLink("Results I", href="/resultshull")),
    ], pills=True, justified=True),
], className="mt-4")

introduction = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Introduction"),
            html.P("""This application provides a comprehensive tool that allows the user to design a sailboat oriented to performance from the very beginning. For doing so, the application operates with a parametric model of the hull that allows easy manipulation through a small number of parameters. At the first stage, the hull is optimized towards the minimum resistance computed in several heel angles. An NSGA II algorithm is responbile to carry out the optimization phase, displaying in the end the most suitable hulls for the user. Based on the best hull, the optimization process is repeated for all the appendages, namely keel and rudder, and sails. At this phase, a Velocity Prediction Program is applied to compute and estimation for velocity."""),
            html.Div([
                html.A('Read More', download='Thesis.pdf',
                       href='/assets/Thesis.pdf'),
                html.Br(), html.Br(),
                dbc.Button(dcc.Link(html.Div("Start the simulation >"),
                                    href=f"/hull", style={'color': 'white'})),
            ]),
        ], md=6, className="justify"),
        dbc.Col([
            html.H2("How it works"),
            html.Br(),
            dbc.Row([
                dbc.Col(html.I(className="icon-tools fa-3x"),
                        md=4, className='update'),
                dbc.Col(html.I(className="icon-adjustments fa-3x"),
                        md=4, className='update'),
                dbc.Col(html.I(className="icon-speedometer fa-3x"),
                        md=4, className='update'),

            ]),
            dbc.Row([
                dbc.Col(html.P(
                    "Set the hull dimensions that will serve as starting point"), md=4, className='update'),
                dbc.Col(html.P(
                    "Configure the genetic algorithm and the parameters to be optimized"), md=4, className='update'),
                dbc.Col(html.P(
                    "Run the optimization. It might take some time depending on your machine"), md=4, className='update'),

            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(html.I(className="icon-bargraph fa-3x"),
                        md=4, className='update'),
                dbc.Col(html.I(className="icon-refresh fa-3x"),
                        md=4, className='update'),
                dbc.Col(html.I(className="icon-search fa-3x"),
                        md=4, className='update'),
            ]),
            dbc.Row([
                dbc.Col(html.P(
                    "Choose one hull based on least resistance performance"), md=4, className='update'),
                dbc.Col(html.P(
                    "Repeat the optimization proccess, but now for appendages and the sailset"), md=4, className='update'),
                dbc.Col(html.P(
                    "View the outcome results and export the best individuals"), md=4, className='update'),
            ]),
        ], md=6),
    ]),
], className="mt-4")

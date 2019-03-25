import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_daq as daq

introduction = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Introduction"),
            html.P("""This application provides a comprehensive tool that allows the user to design a sailboat oriented to performance from the very beginning. For doing so, the application operates with a parametric model of the hull that allows easy manipulation through a small number of parameters. At the first stage, the hull is optimized towards the minimum resistance computed in several heel angles. An NSGA II algorithm is responbile to carry out the optimization phase, displaying in the end the most suitable hulls for the user. Based on the best hull, the optimization process is repeated for all the appendages, namely keel and rudder, and sails. At this phase, a Velocity Prediction Program is applied to compute and estimation for velocity."""),
        ], md=6),
    ]),
], className="mt-4")

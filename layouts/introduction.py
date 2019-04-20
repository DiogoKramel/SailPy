import dash
import dash_bootstrap_components as dbc
import dash_html_components as html


introduction = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Introduction"),
            html.P("This application provides a comprehensive tool that allows the user to design a sailboat oriented to its performance from the very beginning. For doing so, the application operates through a parametric model of the hull that allows easy manipulation through a small number of parameters. At the first stage, the hull is optimized towards the minimum resistance computed in several heel angles and velocities. An NSGA II algorithm is responsible to carry out the optimization phase, displaying, in the end, the most suitable hulls for the user. Based on one hull selected by the user, the optimization process is repeated for appendages, namely keel and rudder, and sails. A first draft for the final sailboat is drawn. At this phase, a Velocity Prediction Program is applied to compute an estimation for velocity that will guide the optimization process. After the analysis is completed, the user may view and export the dimensions set for the entire sailboat"),
            html.Div([
                html.A('Read More', download='thesis.pdf', href='/assets/thesis.pdf'),
            ]),
        ], md=6, className="justify"),
        dbc.Col([
            html.H4("How it works"),
            html.Br(),
			html.Div(className='update', children=[
				dbc.Row([
					dbc.Col(html.I(className="icon-tools fa-2x")),
					dbc.Col(html.I(className="icon-adjustments fa-2x")),
					dbc.Col(html.I(className="icon-speedometer fa-2x")),
				]),
				dbc.Row([
					dbc.Col(html.P("Set the hull dimensions that will serve as a starting point")),
					dbc.Col(html.P("Configure the genetic algorithm and the parameters to be optimized")),
					dbc.Col(html.P("Run the optimization. It might take some time")),
				]),
			]),
            html.Br(),
			html.Div(className='update', children=[
				dbc.Row([
					dbc.Col(html.I(className='icon-bargraph fa-2x')),
					dbc.Col(html.I(className='icon-refresh fa-2x')),
					dbc.Col(html.I(className='icon-search fa-2x')),
				]),
				dbc.Row([
					dbc.Col(html.P("Choose one hull based on the least resistance performance")),
					dbc.Col(html.P("Repeat the optimization process, but now for appendages and sails")),
					dbc.Col(html.P("View the outcome results and export the best individuals")),
				]),
			]),
        ], md=6),
    ]),
], className='mt-4')

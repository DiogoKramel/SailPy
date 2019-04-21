import dash
import dash_bootstrap_components as dbc
import dash_html_components as html


introduction = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Summary"),
            html.P("This application provides a comprehensive set of tools that allow the user to design a sailboat aiming to improve performance from the very beginning. For doing so, the application applies a parametric model of the hull that allows easy manipulation through a small number of parameters in order to generate new study objects. At the first stage, the hull is optimized towards the minimum resistance computed in several heel angles and velocities, whilst respecting constraints of safety and comfort. A Genetic Algorithm is responsible to carry out the optimization phase using default or custom parameters. After finished, all the hulls generated are displayed and the user can choose which is the most suitable. Based on one hull selected, the optimization process is repeated for appendages, namely keel and rudder, and sails. A first draft for the final sailboat can be drawn by the user. At this phase, a Velocity Prediction Program is applied to compute an estimation for velocity that will guide the optimization process. After the analysis is completed, the user may view and export the dimensions set for the entire sailboat."),
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
					dbc.Col(html.P("View the outcome and export the best individuals")),
				]),
			]),
        ], md=6),
    ]),
], className='mt-4')

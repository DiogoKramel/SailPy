import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from callbacks import dimensionshullcall
from callbacks import dimensionshullplots


hull = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4('Main parameters'),
            html.P("Set the category and overall length that will serve to build the regressions for each of the dimensions below. First, the main linear dimensions can be set, later the form coefficients can be adjusted, and lastly refinements on the curvature are performed. Following how the plots behave, you can understand how your choices affect the hull."),
            html.P("Have in mind that the plots are mere representations and tend not to be accurate for extreme cases. Even if the sections are incongruent, you can advance once the limits are respected."),
            dbc.FormGroup([
                dbc.Label('Overall length'),
                html.Div(id='loa-ft', style={'display': 'inline-block'}),
                dcc.Slider(
                    id='loa',
                    min=20,
                    max=55,
                    value=40,
                    step=1,
                    marks={20: '20ft', 25: '25ft', 30: '30ft', 35: '35ft', 40: '40ft', 45: '45ft', 50: '50ft', 55: '55ft'},
                ),
                html.Br(),
            ]),
            html.Div(id='main-dimensions', style={'width': '75%'}),
			html.Details([
				html.Summary('Form Coefficients'),
				html.Div([
					dbc.Label('Midsection Coefficient'),
					dcc.Slider(
						id='cm',
						min=0.65,
						max=0.78,
						value=0.7,
						step=0.01,
						marks={0.65: '0.65', 0.68: '0.68', 0.71: '0.71', 0.74: '0.74', 0.78: '0.78'}
					),
					html.Br(),
					dbc.Label('Block Coefficient'),
					dcc.Slider(
						id='cb',
						min=0.3,
						max=0.4,
						value=0.38,
						step=0.01,
						marks={0.3: '0.3', 0.32: '0.32', 0.34: '0.34', 0.36: '0.36', 0.38: '0.38', 0.4: '0.4'}
					),
					html.Br(),
					dbc.Label('Waterplane Area Coefficient'),
					dcc.Slider(
						id='cwp',
						min=0.68,
						max=0.71,
						value=0.7,
						step=0.01,
						marks={0.68: '0.65', 0.69: '0.69', 0.70: '0.71', 0.71: '0.71'}
					),
					html.Br(), html.Br()
				], className='regularfont')
			]),
            html.Details([
				html.Summary('Hull Adjustments'),
				html.Div([
					dbc.Label('SAC angle at the bow [degrees]'),
					dbc.Input(type='text', id='alpha_f_sac', bs_size='sm', value='{}'.format(round(5, 2))),
					dbc.Label('SAC angle at the stern [degrees]'),
					dbc.Input(type='text', id='alpha_i_sac', bs_size='sm', value='{}'.format(round(25, 2))),
					dbc.Label('Keel curve angle at the bow [degrees]'),
					dbc.Input(type='text', id='angle_keel_bow', bs_size='sm', value='{}'.format(round(20, 2))),
					dbc.Label('Keel curve angle at the stern [degrees]'),
					dbc.Input(type='text', id='angle_keel_stern', bs_size='sm', value='{}'.format(round(35, 2))),
					dbc.Label('Hull bottom angle [degrees]'),
					dbc.Input(type='text', id='beta_n', bs_size='sm', value='{}'.format(round(0, 2)))
				], className='regularfont')
			]),
        ], className = 'justify', md=4),
        dbc.Col([
            html.H4('Lines Drawing'),
            html.Div(dcc.Graph(id='insert-sac', style={'width': 'inherit'})),
            html.Br(),
            html.Div(dcc.Graph(id='insert-wl', style={'width': 'inherit'})),
            html.Br(),
            html.Div(dcc.Graph(id='insert-keel', style={'width': 'inherit'})),
            html.Br(),
            html.Div(dcc.Graph(id='insert-section', style={'width': 'inherit'})),
            html.Br(),
            html.H4('Other calculations'),
            html.Div(id='other-dimensions', className='regularfont', style={'width': '100%'}),
            html.Br(),
            html.H4('Testing fitness according to DELFT Series'),
            html.Div(id='test-lwlbwl', className='regularfont'),
            html.Div(id='test-bwltc', className='regularfont'),
            html.Div(id='test-lwldisp', className='regularfont'),
            html.Div(id='test-loadingfactor', className='regularfont'),
        	html.Div(id='test-prismatic', className='regularfont'),
            html.Div(id='test-feasibility', style={'display': 'block', 'text-align': 'center'}),
        ], className = 'justify', md=8)
    ]),
], className='mt-4',)

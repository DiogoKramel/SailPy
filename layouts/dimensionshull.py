import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from callbacks import dimensionshullcall
# from callbacks import dimensionshullplots


hull = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4('Main parameters'),
            html.P("The first stage of the analysis is setting the main dimensions of the hull. The boat #1 dimensions will be used \
					further in the analysis, whereas the boat #2 can be used to investigate new solutions to reduce resitance."),
            #dbc.FormGroup([
            #    dbc.Label('Overall length'),
            #    html.Div(id='loa-ft', style={'display': 'inline-block'}),
            #    dcc.Slider(
            #        id='loa',
            #        min=20,
            #        max=55,
            #        value=40,
            #        step=1,
            #        marks={20: '20ft', 25: '25ft', 30: '30ft', 35: '35ft', 40: '40ft', 45: '45ft', 50: '50ft', 55: '55ft'},
            #    ),
            #    html.Br(),
            #]),
        ], className = 'justify', md=4),
        dbc.Col([
			html.H4('Main Dimensions'),
			html.Div([
				dbc.Row([
					dbc.Col([
						html.H5('Hull #1'),
						dbc.Label('Waterline Length [m]'),
						dbc.Input(type='text', id='lwl', bs_size='sm', value='{}'.format(round(10,2))),
						#html.Div(id='limits-lwl', className='limits'),
						dbc.Label('Waterline Beam [m]'),
						dbc.Input(type='text', id='bwl', bs_size='sm', value='{}'.format(round(3.17,2))),
						dbc.Label('Draft Canoe Body [m]'),
						dbc.Input(type='text', id='tc', bs_size='sm', value='{}'.format(round(0.57,2))),
						dbc.Label('Displacement [m3]'),
						dbc.Input(type='text', id='disp', bs_size='sm', value='{}'.format(round(8.17,2))),
						#html.Div(id='limits-tc', className='limits'),
						dbc.Label('Longitudinal Centre of Buoyancy (LCB) [m]'),
						dbc.Input(type='text', id='lcb', bs_size='sm', value='{}'.format(round(5,2))),
						#html.Div(id='limits-lcb', className='limits'),
						dbc.Label('Longitudinal Centre of Flotation (LCF) [m]'),
						dbc.Input(type='text', id='lcf', bs_size='sm', value='{}'.format(round(4,2))),
						#html.Div(id='limits-lcf', className='limits'),
						html.Br(),
					], className = 'justify', md=5),
					dbc.Col([], className = 'justify', md=2),
					dbc.Col([
						html.H5('Hull #2 [Experiment]'),
						dbc.Label('Waterline Length [m]'),
						dbc.Input(type='text', id='lwl2', bs_size='sm', value='{}'.format(round(10,2))),
						#html.Div(id='limits-lwl', className='limits'),
						dbc.Label('Waterline Beam [m]'),
						dbc.Input(type='text', id='bwl2', bs_size='sm', value='{}'.format(round(3.17,2))),
						dbc.Label('Draft Canoe Body [m]'),
						dbc.Input(type='text', id='tc2', bs_size='sm', value='{}'.format(round(0.57,2))),
						dbc.Label('Displacement [m3]'),
						dbc.Input(type='text', id='disp2', bs_size='sm', value='{}'.format(round(8.17,2))),
						#html.Div(id='limits-tc', className='limits'),
						dbc.Label('Longitudinal Centre of Buoyancy (LCB) [m]'),
						dbc.Input(type='text', id='lcb2', bs_size='sm', value='{}'.format(round(5,2))),
						#html.Div(id='limits-lcb', className='limits'),
						dbc.Label('Longitudinal Centre of Flotation (LCF) [m]'),
						dbc.Input(type='text', id='lcf2', bs_size='sm', value='{}'.format(round(4,2))),
						#html.Div(id='limits-lcf', className='limits'),
						html.Br(),
					], className = 'justify', md=5),
				]),
			], className='regularfont'),
			html.H4('Form Coefficients'),
			html.Div([
				dbc.Row([
					dbc.Col([
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
						dbc.Label('Prismatic Coefficient'),
						dcc.Slider(
							id='cp',
							min=0.52,
							max=0.6,
							value=0.58,
							step=0.01,
							marks={0.52: '0.52', 0.54: '0.54',0.56: '0.56', 0.58: '0.58', 0.60: '0.60'}
						),
						html.Br(),
						dbc.Label('Waterplane Area Coefficient'),
						dcc.Slider(
							id='cwp',
							min=0.65,
							max=0.9,
							value=0.75,
							step=0.01,
							marks={0.65: '0.65', 0.70: '0.70', 0.80: '0.80', 0.90: '0.90'}
						),
					], className = 'justify', md=5),
					dbc.Col([], className = 'justify', md=2),
					dbc.Col([
						dbc.Label('Midsection Coefficient'),
						dcc.Slider(
							id='cm2',
							min=0.65,
							max=0.78,
							value=0.7,
							step=0.01,
							marks={0.65: '0.65', 0.68: '0.68', 0.71: '0.71', 0.74: '0.74', 0.78: '0.78'}
						),
						html.Br(),
						dbc.Label('Prismatic Coefficient'),
						dcc.Slider(
							id='cp2',
							min=0.52,
							max=0.6,
							value=0.58,
							step=0.01,
							marks={0.52: '0.52', 0.54: '0.54',0.56: '0.56', 0.58: '0.58', 0.60: '0.60'}
						),
						html.Br(),
						dbc.Label('Waterplane Area Coefficient'),
						dcc.Slider(
							id='cwp2',
							min=0.65,
							max=0.90,
							value=0.75,
							step=0.01,
							marks={0.65: '0.65', 0.70: '0.70', 0.80: '0.80', 0.90: '0.90'}
						),
					], className = 'justify', md=5),
				]),
			], className='regularfont'),
			html.Br(),html.Br(),
			html.H4('Resistance comparison'),
			html.Div(dcc.Graph(id='resistance-comparison')),
            #html.H4('Other calculations'),
            #html.Div(id='other-dimensions', className='regularfont', style={'width': '100%'}),
            #html.Br(),
            #html.H4('Testing fitness according to DELFT Series'),
            #html.Div(id='test-lwlbwl', className='regularfont'),
            #html.Div(id='test-bwltc', className='regularfont'),
            #html.Div(id='test-lwldisp', className='regularfont'),
            #html.Div(id='test-loadingfactor', className='regularfont'),
        	#html.Div(id='test-prismatic', className='regularfont'),
            #html.Div(id='test-feasibility', style={'display': 'block', 'text-align': 'center'}),
        ], className = 'justify', md=8)
    ]),
], className='mt-4',)

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
            html.P("Set the category and overall length that will serve to build the regressions for each of the dimensions below. First, the main linear dimensions can be set, later the form coefficients can be adjusted, and lastly refinements on the curvature are performed. Following how the plots behave, you can understand how your choices affect the hull"),
            html.P("Have in mind that the plots are mere representations and tend not to be accurate for extreme cases. Even if the sections are incongruent, you can advance once the limits are respected"),
            dbc.FormGroup([
                dbc.Label('Category'),
                dbc.RadioItems(
                    id='boat-category',
                    options=[
                        {'label': 'Cruiser', 'value': 'cruiser'},
                        {'label': 'Racer [WIP]', 'value': 'racer'},
                    ],
                    value='cruiser',
                    inline=True,
                    className='regularfont'
                ),
                html.Br(),
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
            html.Div(id='form-coefficients', style={'width': '75%'}),
            html.Div(id='hull-adjustmetns', style={'width': '75%'}),
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
            html.Div(id='test-feasibility'),
        ], className = 'justify', md=8)
    ]),
], className='mt-4',)

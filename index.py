import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash_table_experiments import DataTable

from app import app
from layout import navbar, stepbar, introduction, bottombar
from hulllayout import hull
from optimizationlayout import optimizationhull
from resultshulllayout import resultshull, resultsplus


app.title = 'App Name'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Meta(name='viewport', content='width=device-width, initial-scale=1.0',
              title='Swellow Application. Developed by Diogo Kramel.'),
    #html.Link(href='/assets/static/favicon.ico'),
    navbar,
    stepbar,
    dbc.DropdownMenuItem(divider=True),
    html.Div(id='page-content'),
    html.Br(), html.Br(), html.Br(),
    dbc.DropdownMenuItem(divider=True),
    bottombar
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == 'index' or pathname == 'introduction':
        return introduction
    elif pathname == 'hull':
        return hull
    elif pathname == 'optimizationhull':
        return optimizationhull
    elif pathname == 'resultshull':
        return resultshull, resultsplus
    else:
        return '404'


if __name__ == "__main__":
    app.run_server(debug=True)

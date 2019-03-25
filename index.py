import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from dash_table_experiments import DataTable

from app import app
from layout import navbar, stepbar, introduction, bottombar
#from hulllayout import hull
#from optimizationlayout import optimizationhull
#from resultshulllayout import resultshull, resultsplus


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/index' or pathname == '/introduction':
        return introduction
    else:
        return introduction


if __name__ == "__main__":
    app.run_server(debug=True)

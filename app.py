import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config['suppress_callback_exceptions'] = True

external_css = ["https://use.fontawesome.com/releases/v5.7.2/css/all.css", "assets/fonts/et-line-font/style.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == '__main__':
    app.run_server(debug=True)
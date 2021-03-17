# -*- coding: utf-8 -*-

# Run this app with `python app3.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/ 

# based on app3.py and ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line

from flask import Flask
from os import environ

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)

app.layout = html.Div([
    dcc.Markdown('''
        ### image annotation

        #### Purpose

        Try out images and user annotations.

        ----------
        '''),

    html.Label('No. cycles:'),
    dcc.Slider(id='ncycles', min=2, max=10, value=3, step=0.5,
        marks={2:'2', 4:'4', 6:'6', 8:'8', 10:'10'}
        ),        
    dcc.Graph(id='indicator-graphic'),

    dcc.Markdown('''
        ----
        
        ### Questions students could consider

        Later
  
        ''')
], style={'width': '900px'}
)

# The callback function with it's app.callback wrapper.
@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('ncycles', 'value'),  
    )    
def update_graph(ncycles):
    # Create figure
    fig = go.Figure()

    # Add trace
    fig.add_trace(
        go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1])
    )

    # Add images
    fig.add_layout_image(
            dict(
                source="file://C:/Users/fhmjo/repos/image_annot01/agerange-exercise1.jpg",
                xref="x",
                yref="y",
                x=0,
                y=3,
                sizex=2,
                sizey=2,
                sizing="stretch",
                opacity=0.5,
                layer="below")
    )

    # Set templates
    fig.update_layout(template="plotly_white")

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

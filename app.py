# -*- coding: utf-8 -*-

# Run this app with `python app3.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/ 

# based on app3.py and ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line
# modebar buttons: https://plotly.com/python/configuration-options/ (remove, or add shape-drawing)
# add text (your name) https://community.plotly.com/t/how-to-add-a-text-area-with-custom-text-as-a-kind-of-legend-in-a-plotly-plot/24349


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

    html.Label('Pen thickness (pixels)'),
    dcc.Slider(id='penthick', min=3, max=15, value=9, step=2,
        marks={3:'3 pixels', 5:'5', 7:'7', 9:'9', 11:'11', 13:'13', 15:'15'}
        ),        
    dcc.Graph(
        id='indicator-graphic',
        config={
                'staticPlot': False,      # True, False
                'scrollZoom': False,      # True, False
                'doubleClick': 'reset',   # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,         # True, False
                'displayModeBar': True,   # True, False, 'hover'
                'watermark': False,
                'modeBarButtonsToRemove': ['resetAxis', 'pan2d', 'resetScale2d', 'select2d', 'lasso2d', 'zoom2d', 
                                            'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'hoverCompareCartesian', 'hoverClosestCartesian'],
                'modeBarButtonsToAdd': ['drawline', 'eraseshape' ]
            }
    ),

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
    Input('penthick', 'value'),  
    )    
def update_graph(penthick):
    # Create figure
    fig = go.Figure()

    # Add trace
    # fig.add_trace(go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1]) )

    # Add images
    # "agerange-exercise1.jpg" is 500 x 340 or 
    fig.add_layout_image(
            dict(
                source="https://raw.githubusercontent.com/fhmjones/dash_ImageAnnot01/main/assets/agerange-exercise1.jpg",
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                opacity=1,
                layer="above")
    )

    # Set templates
    # fig.update_layout(template="plotly_white")
    fig.update_layout(width=800, height=600)
    fig.update_layout(annotations=[
        go.layout.Annotation(
            text='Your name',
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=0,
        )
    ])
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    # Set dragmode and newshape properties; add modebar buttons
    fig.update_layout(
        dragmode='drawline',
        newshape=dict(line_color='magenta', line_width=penthick),
        title_text='Click-Drag to draw. Point click to select line before choosing "erase".'
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

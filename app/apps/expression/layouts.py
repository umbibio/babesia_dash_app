from dash import dcc
from dash import html

from plotly.colors import sample_colorscale, get_colorscale

import dash_bootstrap_components as dbc

from data import species_names, species_keys

menu = [
    html.Br(),
    dbc.Label("Select Species:", html_for='species-dropdown'),
    dbc.Select(id='species-dropdown',
        options=[{'label':fn, 'value':sn} for sn, fn in species_names.items()],
        value=species_keys[0]),
    html.Br(),
    # dbc.Label("Color by", html_for='color-by-radio'),
    # dbc.RadioItems(id='color-by-radio',
    #     options=[{'label': x, 'value': x} for x in ['Gene', 'Phase']],
    #     value='Gene',
    #     inline=True),
    # html.Br(),
    dbc.Label("Plot type", html_for='dimred-radio'),
    dbc.RadioItems(id='dimred-radio',
        options=[{'label': x, 'value': x} for x in ['PCA', 'UMAP']],
        value='PCA',
        inline=True),
    dbc.RadioItems(id='2d3d-radio',
        options=[{'label': x, 'value': x} for x in ['2D', '3D']],
        value='2D',
        inline=True),
    html.Br(),
    html.Div(id='expression-gene-dropdown-container', children=[
        dbc.Label([
            "Select Gene:",
            dbc.Button("Example", id='expression-gene-example-button', size='sm', color='primary', outline=True),
        ], html_for='expression-gene-dropdown', style={'display': 'flex', 'justify-content': 'space-between'}),
        dcc.Dropdown(id='expression-gene-dropdown', options=[], placeholder='Search...'),
        
    ], style={'display': 'none'}),
]


body = [
    html.H3('Expression'),
    dbc.Spinner([ dcc.Graph(
        id='expression-graph', 
        figure={'layout': { 'height': 700 } },
    )], type='border', fullscreen=False, color='primary', delay_hide=100, ),
]


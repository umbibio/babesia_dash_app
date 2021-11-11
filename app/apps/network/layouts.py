from dash import dcc
from dash import html
from dash import dash_table
import dash_cytoscape as cyto

import dash_bootstrap_components as dbc

from data import species_names, species_keys


menu = [
    html.Br(),
    dbc.Label("Species", html_for='network-species-dropdown'),
    dbc.Select(id='network-species-dropdown',
        options=[{'label':fn, 'value':sn} for sn, fn in species_names.items()],
        value=species_keys[0]),
    html.Br(),
]


body = [
    html.H3('Network'),
    cyto.Cytoscape(
        id='network-graph',
        layout={
            'name': 'cose',
            'idealEdgeLength': 100,
            'nodeOverlap': 20,
            'refresh': 20,
            'fit': True,
            'padding': 30,
            'randomize': True,
            'componentSpacing': 100,
            'nodeRepulsion': 400000,
            'edgeElasticity': 100,
            'nestingFactor': 5,
            'gravity': 80,
            'numIter': 1000,
            'initialTemp': 200,
            'coolingFactor': 0.95,
            'minTemp': 1.0,
            'animate': True,
        },
        style={'width': '100%', 'height': '500px'},
        responsive=True,
        elements=[],
    ),
    dash_table.DataTable(id='network-nodes-table', page_size=12,
        columns=[
            {'name': 'GeneID', 'id': 'GeneID', 'type': 'text'},
            {'name': 'degree', 'id': 'degree', 'type': 'numeric'},
            {'name': 'z.score', 'id': 'z.score', 'type': 'numeric'},
            {'name': 'ProductDescription', 'id': 'ProductDescription', 'type': 'text'},
            {'name': 'phase', 'id': 'phase', 'type': 'text'},
        ],
        style_table={'overflowX': 'auto'},
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_action="native",
        row_selectable='multi',
        selected_rows=[],
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['GeneID', 'ProductDescription', 'phase']
        ],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{X} >= 0.5',
                },
                'backgroundColor': 'BlanchedAlmond',
                # 'color': 'black'
            },
            {
                'if': {
                    'filter_query': '{X} < 0.5',
                },
                'backgroundColor': 'AliceBlue',
                # 'color': 'black'
            }
        ],
    )
]


from dash import dcc
from dash import html
from dash import dash_table
import dash_cytoscape as cyto
from numpy import histogram_bin_edges
from plotly.colors import sample_colorscale, get_colorscale

import dash_bootstrap_components as dbc

from data import species_names, species_keys
from apps.network.common import table_columns, phase_abbrv, phase_names, phase_colors


menu = [
    html.Br(),
    dbc.Label("Species", html_for='network-species-dropdown'),
    dbc.Select(id='network-species-dropdown',
        options=[{'label':fn, 'value':sn} for sn, fn in species_names.items() if sn != 'bmic'],
        value=species_keys[0]),
    html.Br(),
    dbc.Table(id='nodes-color-legend-table',children=[
        html.Thead(html.Tr( [
            html.Th('Legend', colSpan=2),
        ] )),
        html.Tbody([
            html.Tr([
                    html.Td( html.Span([html.I(className="bi bi-circle-fill", style={'color': color})]),),
                    html.Td(phase),
                ],
                # draggable='false',
            )
            for phase, color in zip(phase_names, phase_colors)
        ])

    ], hover=False),
    dbc.Table(id='selected-nodes-table', hover=False),
]


cytoscape_stylesheet = [
    {
        "selector": "node",
        "style": {
            "width": "mapData(size, 1, 50, 2, 100)",
            "height": "mapData(size, 1, 50, 2, 100)",
            "content": "data(label)",
            "font-size": "16px",
            "text-valign": "center",
            "text-halign": "center",
            # "min-zoomed-font-size": "14px",
        }
    },
] + [
    {
        "selector": f".{phase}",
        'style': {
            'background-color': color,
        }
    }
    for phase, color in zip(phase_abbrv, phase_colors)
]

def make_filter_popover(name, input_component, delay, **kvargs):
    return html.Div([
        dbc.Button('Filter', id=f'network-nodes-table-filter-{name}-toggle-button', color='primary', size='sm'),
        dbc.Popover(
            [
                dbc.PopoverBody([
                    html.P(id=f'network-nodes-table-filter-{name}-form-message'),
                    input_component(id=f'network-nodes-table-filter-{name}', **kvargs),
                ]),
            ],
            id=f'network-nodes-table-filter-{name}-popover',
            target=f'network-nodes-table-filter-{name}-toggle-button',
            trigger='legacy',
            delay={'show': 0, 'hide': 0},
        ),
    ]),

filter_inputs = {
    'GeneID': dbc.Input(id='network-nodes-table-filter-GeneID', placeholder='Filter ...', size='sm'),
    'degree':  make_filter_popover('degree', dcc.RangeSlider, 10000, pushable=True, step=1),
    'z.score': make_filter_popover('zscore', dcc.RangeSlider, 10000, pushable=True, step=0.01),
    'ProductDescription': dbc.Input(id='network-nodes-table-filter-ProductDescription', placeholder='Filter ...', size='sm'),
    'phase': make_filter_popover('phase', dbc.Checklist, 3000),
}

body = [
    dcc.Store(id='dummy-store-1'),
    dcc.Store(id='dummy-store-2'),
    dcc.Store(id='dummy-store-3'),
    dcc.Store(id='label-offset-store', data=16),
    dcc.Store(id='label-scale-store', data=0),
    dcc.Store(id='network-nodes-info'),
    dcc.Store(id='selected-network-nodes', data=[]),
    dcc.Store(id='network-nodes-table-sort-column-values-state', data=[0 for _ in table_columns]),
    html.H3('Network'),
    dbc.Row([dbc.Col([
        dbc.Card(
            [
                dbc.Spinner([ cyto.Cytoscape(
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
                        'animate': False,
                    },
                    # style={'width': '100%', 'height': '500px', 'backgroundColor': 'var(--bs-gray-200)'},
                    style={'width': '100%', 'height': '500px', 'backgroundColor': 'var(--bs-white)'},
                    responsive=False,
                    elements=[],
                    stylesheet=cytoscape_stylesheet, ), ], id=f'loading-network-graph', type='border', fullscreen=False, color='primary', delay_hide=0,),
                dbc.ButtonGroup(
                    [
                        dbc.Button([ 'Settings ' ], id='graph-settings-toggle-button', size='sm', color='link'),
                        dbc.Button([ 'Save as PNG ', html.Span([html.I(className="bi bi-download")])], id='download-cytoscape-image-button', size='sm', style={'display': 'none'}),
                    ], class_name='position-absolute top-0 end-0',
                ),
            ], class_name='position-relative'),
    ],)], class_name='mb-4'),
    dbc.Collapse(
        dbc.Row([dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4('Graph Settings')),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Label('Adjust label font weight', width=4),
                        dbc.Col([
                            dbc.Input(id='node-label-font-weight', type='number', size='sm', value=600, min=100, max=900, step=100),
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Label('Adjust label font size', width=4),
                        dbc.Col([
                            dbc.Input(id='node-label-font-size', type='number', size='sm', value=16, min=2, step=2),
                        ], width=6),
                    ]),
                    # dbc.Row([
                    #     dbc.Label('Adjust label font size', width=4),
                    #     dbc.Col([
                    #         dbc.ButtonGroup([
                    #             dbc.Button([ html.Span([html.I(className="bi bi-fonts"), html.I(className="bi bi-dash")])], id='decrease-cytoscape-label-offset', size='sm'),
                    #             dbc.Button([ html.Span([html.I(className="bi bi-fonts"), html.I(className="bi bi-plus")])], id='increase-cytoscape-label-offset', size='sm'),
                    #         ]),
                    #     ], width=6),
                    # ]),
                    dbc.Row([
                        dbc.Label('Adjust label scale prop. to node degree', width=4),
                        dbc.Col([
                            dbc.ButtonGroup([
                                dbc.Button([ html.Span([html.I(className="bi bi-fonts"), html.I(className="bi bi-dash")])], id='decrease-cytoscape-label-scale', size='sm'),
                                dbc.Button([ html.Span([html.I(className="bi bi-fonts"), html.I(className="bi bi-plus")])], id='increase-cytoscape-label-scale', size='sm'),
                            ]),
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Label('Minimum node degree to show label', width=4),
                        dbc.Col([
                            dbc.Input(id='min-node-size-label-filter', type='number', size='sm', value=4),
                        ], width=6),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button('Apply', id='apply-graph-settings', size='sm'),
                        ], width={"size": 6, "offset": 4}),
                    ]),
                ]),
            ]),
        ])], class_name='mb-4'),
    id='graph-settings-collapse', is_open=False,),
    dbc.Row([dbc.Col([
        dbc.Card([
            dbc.CardHeader(html.H4('Genes in network')),
            dbc.CardBody([
                dbc.Row(dbc.Col(
                    dbc.Table([
                        html.Thead([
                            html.Tr([ html.Th([col['name'], ' ',  html.Span([html.I(className="bi bi-sort-alpha-down sort-icon", id={'type': 'network-nodes-table-sort-column-values', 'id': col['id']})]),], style=col['header_style']) for col in table_columns ]),
                            html.Tr([ html.Th(
                                filter_inputs[col['id']]
                            ) for col in table_columns ]),
                        ])
                    ],
                    id='network-nodes-table-header',
                    class_name='mb-0'),
                )),
                dbc.Row(dbc.Col(
                    dbc.Spinner([

                    dbc.Table(id='network-nodes-table', hover=True),

                    ], id=f'loading-network-nodes-table', type='border', fullscreen=False, color='primary', delay_hide=0,),
                )),
                dbc.Row([
                    dbc.Col([
                        dbc.Pagination(id='network-nodes-table-pagination', active_page=1, max_value=2, first_last=True, previous_next=True, fully_expanded=False, size='sm', class_name='primary outline'),
                    ], width={'offset': 6, 'size': 4}, ),
                    dbc.Col([
                        html.Div(dbc.RadioItems(
                            id='network-nodes-table-page-size-radio',
                            class_name="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-sm btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {"label": "10", "value": 10},
                                {"label": "20", "value": 20},
                                {"label": "50", "value": 50},
                            ],
                            value=10,
                        ), className='radio-group'),
                    ], width={'size': 2}, ),
                ]),
            ]),
        ]),
    ],)], class_name='mb-4'),
]


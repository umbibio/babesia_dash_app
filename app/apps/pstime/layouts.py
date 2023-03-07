from dash import dcc
from dash import html

import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from app import db
from data import species_keys, species_names
from apps.pstime.common import make_sc_plot


# read ortholod gene ids for all species
ids_set_list = [
    set(db.select(key, 'meta_gene_orth_genes', cols=['GeneID']).GeneID.to_list())
    for key in species_keys if key != 'bmic']
ids_intersection = list(set.intersection(*ids_set_list))
ids_intersection.sort()
del(ids_set_list)

menu = [
    html.Br(),
    # dbc.Label("Select Gene:", html_for='pstime-gene-dropdown'),
    dbc.Label([
        "Select Gene:",
        dbc.Button("Example", id='pstime-gene-example-button', size='sm', color='primary', outline=True),
    ], html_for='pstime-gene-dropdown', style={'display': 'flex', 'justify-content': 'space-between'}),
    dcc.Dropdown(
        id='pstime-gene-dropdown',
        options=[{'label': g, 'value': g} for g in ids_intersection],
        value=None,
        placeholder='Search...'),
    # dbc.Button(['click for example'], id='pstime-gene-example-button', size='sm', color='link'),
]


body = [
    # html.Div([dcc.Store(id={ 'type': 'mata-data-orth-genes', 'key': key}, data=species_data[key]) for key in species_keys]),
    # html.Div([dcc.Store(id={ 'type': 'pstime-expr-graph-figure-data', 'key': key}, data=[]) for key in species_keys]),
    # html.Div([dcc.Store(id={ 'type': 'pstime-expr-graph-figure-layout', 'key': key}, data={}) for key in species_keys]),
    html.H3('Pseudo-time Expression'),
    html.Div(id='pstime-graphs-container', children=[
        dbc.Row(dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4(species_names[key])),
            dbc.CardBody(dbc.Row([
                dbc.Col([
                    dbc.Spinner([
                        dcc.Graph(
                            id={'type': 'pstime-expr-graph', 'key': key},
                            figure=make_sc_plot(key), animate=False),
                    ], id=f'loading-pstime-expr-graph-{key}', type='border', fullscreen=False, color='primary', delay_hide=100,),
                ], width=6),
                dbc.Col([
                    dbc.Spinner([
                        dcc.Graph(
                            id={'type': 'pstime-expr-time-curve', 'key': key},
                            figure={'layout': { 'height': 450, "xaxis": { "visible": 'false' }, "yaxis": { "visible": 'false' }, } },),
                    ], id=f'loading-pstime-expr-time-curve-{key}', type='border', fullscreen=False, color='primary', delay_hide=100,),
                ], width=6),
            ])),
        ])), class_name="mb-4")
        for key in species_keys if key != 'bmic'
    ], style={'display': 'block'}),
]


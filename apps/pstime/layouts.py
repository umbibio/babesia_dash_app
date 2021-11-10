from dash import dcc
from dash import html

import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from app import db
from data import species_keys, species_names


# read ortholod gene ids for all species
ids_set_list = [
    set(db.select(key, 'meta_gene_orth_genes', cols=['GeneID']).GeneID.to_list())
    for key in species_keys]
ids_intersection = list(set.intersection(*ids_set_list))
ids_intersection.sort()
del(ids_set_list)

menu = [
    dbc.Label("Gene", html_for='species-dropdown'),
    dcc.Dropdown(
        id='gene-dropdown',
        options=[{'label': g, 'value': g} for g in ids_intersection],
        value=None),
]


body = [
    html.H3('Pseudo-time Expression'),
    html.Div(id='pstime-graphs-container', children=[
        dbc.Row(dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4(species_names[key])),
            dbc.CardBody(dbc.Row([
                dbc.Col(dcc.Graph(
                    id={'type': 'pstime-expr-graph', 'key': key},
                    style={'display': 'none'},
                    figure=go.Figure(),
                ), width=5),
                dbc.Col(dcc.Graph(
                    id={'type': 'pstime-expr-time-curve', 'key': key},
                    style={'display': 'none'},
                    figure=go.Figure(),
                ), width=7),
            ])),
        ])), className="mb-4")
        for key in species_keys
    ], style={'display': 'block'}),
]


import pandas as pd
from dash.exceptions import PreventUpdate

from dash import callback_context as ctx
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db


@app.callback(
    Output('network-nodes-table', 'data'),
    Input('network-species-dropdown', 'value'), )
def update_table(species):
     df = db.select(species, 'node_info')
     return df.to_dict('records')


@app.callback(
    Output('network-graph', 'elements'),
    Input('network-nodes-table', 'derived_virtual_selected_rows'),
    State('network-species-dropdown', 'value'),
    State('network-nodes-table', 'data'),)
def update_graph(derived_virtual_selected_rows, species, data):
    if not data:
        return []

    src = pd.DataFrame(data).iloc[derived_virtual_selected_rows]

    edges = db.select(species, 'edge_list', cols=['src', 'trg'], src=src.GeneID.to_list())
    edges = pd.DataFrame(edges)

    src_nodes = set(edges.src)
    trg_nodes = set(edges.trg)
    nodes = list(set.union(src_nodes, trg_nodes))
    
    nodes = [
        # The nodes elements
        {'data': {'id': gene_id, 'label': gene_id},}
        for gene_id in nodes
    ]

    edges = [
        {'data': {'source': src, 'target': trg}}

        for src, trg in edges.values
    ]

    return nodes + edges
    

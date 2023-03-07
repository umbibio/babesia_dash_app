import json
from dash.html.Header import Header
from dash.html.Pre import Pre
import numpy as np
import pandas as pd
from dash.exceptions import PreventUpdate

from dash import html
from dash import callback_context as ctx
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

import dash_bootstrap_components as dbc

from app import app, db
from apps.network.common import table_columns, phase_color_dict


@app.callback(
    Output('network-nodes-info', 'data'),
    Output('network-nodes-table-filter-phase', 'options'),
    Output('network-nodes-table-filter-degree', 'min'),
    Output('network-nodes-table-filter-degree', 'max'),
    Output('network-nodes-table-filter-degree', 'value'),
    Output('network-nodes-table-filter-degree', 'marks'),
    Output('network-nodes-table-filter-zscore', 'min'),
    Output('network-nodes-table-filter-zscore', 'max'),
    Output('network-nodes-table-filter-zscore', 'value'),
    Output('network-nodes-table-filter-zscore', 'marks'),
    Output('network-nodes-table-pagination', 'active_page'),
    Input('network-species-dropdown', 'value'), )
def update_table_data(species):
    df = db.select(species, 'node_info').reset_index()

    unique_phases = df['phase'].unique()
    unique_phases.sort()
    phase_options = [{'label': v, 'value': v} for v in unique_phases]

    degree_value = [0, df['degree'].max()]
    degree_min, degree_max = degree_value
    degree_marks = {v: f'{v}' for v in range(degree_min, degree_max+1, 10)}

    zscore_value = [df['z.score'].min().round(2)-0.01, df['z.score'].max().round(2)+0.01]
    zscore_min, zscore_max = zscore_value
    zscore_marks = {v: f'{v:.1f}' for v in np.linspace(*zscore_value, 5)}

    active_page = 1
    return df.to_dict('records'), phase_options, degree_min, degree_max, degree_value, degree_marks, zscore_min, zscore_max, zscore_value, zscore_marks, active_page


@app.callback(
    Output('network-graph', 'elements'),
    Output('download-cytoscape-image-button', 'style'),
    Input('selected-network-nodes', 'data'),
    State('network-species-dropdown', 'value'),
    State('network-nodes-info', 'data'),
    Input('min-node-size-label-filter', 'value'), )
def update_graph(selected_rows, species, data, min_node_size_label_filter):
    if not data or not selected_rows:
        return [], {'display': 'none'}

    src = pd.DataFrame(data)
    selected_src = src.iloc[selected_rows]

    edges = db.select(species, 'edge_list', cols=['src', 'trg'], where=dict(src=selected_src.GeneID.to_list()))
    edges = pd.DataFrame(edges)

    src_nodes = set(edges.src)
    trg_nodes = set(edges.trg)
    nodes = src.loc[src.GeneID.isin(set.union(src_nodes, trg_nodes))]
    
    nodes = [
        # The nodes elements
        {
            'data': {
                'id': node.GeneID,
                'label': node.GeneID if node.degree >= min_node_size_label_filter else '',
                'size': node.degree,
            },
            'classes': node.phase,
        }
        for _, node in nodes.iterrows()
    ]

    edges = [
        {'data': {'source': src, 'target': trg}}

        for src, trg in edges.values
    ]

    return nodes + edges, {}


@app.callback(
    Output('selected-nodes-table', 'children'),
    State('network-nodes-info', 'data'),
    Input('selected-network-nodes', 'data'), )
def update_selected_nodes_table(node_info_data, selected_nodes):
    if not node_info_data:
        raise PreventUpdate

    df = pd.DataFrame(node_info_data).iloc[selected_nodes]
    if len(df) > 0:
        sel_header = [
            html.Thead(html.Tr( [
                html.Th('Selected nodes', colSpan=2),
            ] ))
        ]
    else:
        sel_header = []

    sel_body = [
        html.Tbody([
            html.Tr([
                html.Td(
                    html.Span([html.I(className="bi bi-x-circle-fill danger",
                                      id={'type': 'remove-selected-network-nodes', 'index': row['index']})]),
                    className='remove-selected', ),
                html.Td(row.GeneID),
            ],
            draggable='true', )
            for i, row in df.iterrows()
        ])
    ]
    return sel_header + sel_body


@app.callback(
    Output({'type': 'net-node-table-tr', 'index': MATCH}, 'style'),
    Output({'type': 'net-node-table-tr', 'index': MATCH}, 'className'),
    State({'type': 'net-node-table-tr', 'index': MATCH}, 'id'),
    Input('selected-network-nodes', 'data'), )
def update_selected_rows(id, data):
    if id['index'] in data:
        style = {"fontWeight": 'bold'}
        className = 'table-active'
    else:
        style = {"fontWeight": 'normal'}
        className = ''
    return style, className


@app.callback(
    Output('selected-network-nodes', 'data'),
    Output('interaction-with-table-count', 'data'),
    Output('network-clear-all-selected-genes', 'style'),
    Input({'type': 'net-node-table-tr', 'index': ALL}, 'n_clicks'),
    Input({'type': 'remove-selected-network-nodes', 'index': ALL}, 'n_clicks'),
    State('selected-network-nodes', 'data'),
    Input('network-species-dropdown', 'value'), 
    Input('network-nodes-table', 'children'),
    State('interaction-with-table-count', 'data'),
    Input('network-clear-all-selected-genes', 'n_clicks'))
def update_selected_rows(row_n_clicks, sel_n_clicks, data, species, on_screen_table, interaction_count, clear_all):

    print(ctx.triggered[0]['prop_id'])
    if ctx.triggered[0]['prop_id'] == '.':
        print('cond 1')
        print(row_n_clicks)
        raise PreventUpdate


    if ctx.triggered[0]['prop_id'] == 'network-nodes-table.children' and interaction_count == 0:
        if data == [0]:
            raise PreventUpdate
        return [0], interaction_count, {'display': 'none'}

    if ctx.triggered[0]['prop_id'] == 'network-species-dropdown.value':
        print('cond 2')
        if data == [0]:
            raise PreventUpdate
        return [0], interaction_count, {'display': 'none'}

    if ctx.triggered[0]['prop_id'] == 'network-clear-all-selected-genes.n_clicks':
        return [], interaction_count, {'display': 'none'}

    if len(ctx.triggered) == 1:
        print('cond 3')
        # print(ctx.triggered)
        # print(len(ctx.triggered))
        id_str = ctx.triggered[0]['prop_id'].split('.')[0]
        id = json.loads(id_str)
        index = id['index']

    else:
        print('cond 3 else')
        # print(ctx.triggered)
        # print(len(ctx.triggered))
        raise PreventUpdate

    if index < 0:
        print('cond 4')
        raise PreventUpdate

    if index not in data:
        print('cond 5')
        data.append(index)
        interaction_count += 1
    else:
        print('cond 5 else')
        data.remove(index)
        interaction_count += 1

    if len(data) > 1:
        clear_all_style = {'display': 'block'}
    else:
        clear_all_style = {'display': 'none'}

    return data, interaction_count, clear_all_style


@app.callback(
    Output('network-nodes-table-sort-column-values-state', 'data'),
    Input({'type': 'network-nodes-table-sort-column-values', 'id': ALL}, 'n_clicks'), )
def update_sort_state(n_clicks):
    return [n % 3 if n else 0 for n in n_clicks]


@app.callback(
    Output({'type': 'network-nodes-table-sort-column-values', 'id': ALL}, 'className'),
    Input('network-nodes-table-sort-column-values-state', 'data'), )
def update_sort_icons_shape(sort_state):
    icons = [
        "bi bi-sort-{}-down sort-icon text-secondary",
        "bi bi-sort-{}-down sort-icon text-primary",
        "bi bi-sort-{}-up sort-icon text-primary",
    ]
    return [icons[s].format(c['type']) for s, c in zip(sort_state, table_columns)]


@app.callback(
    Output('network-nodes-table', 'children'),
    Output('network-nodes-table-pagination', 'max_value'),
    Output('network-nodes-table-filter-degree-form-message', 'children'),
    Output('network-nodes-table-filter-zscore-form-message', 'children'),
    Input('network-nodes-info', 'data'),
    Input('network-nodes-table-pagination', 'active_page'),
    Input('network-nodes-table-page-size-radio', 'value'),
    Input('network-nodes-table-filter-GeneID', 'value'),
    Input('network-nodes-table-filter-degree', 'value'),
    Input('network-nodes-table-filter-zscore', 'value'),
    Input('network-nodes-table-filter-ProductDescription', 'value'),
    Input('network-nodes-table-filter-phase', 'value'),
    Input('network-nodes-table-sort-column-values-state', 'data'),
    State('selected-network-nodes', 'data'), )
def update_info_tables(data, page, page_size, geneid_filter, degree_filter, zscore_filter, description_filter, phase_filter, sort_state, selected_nodes):

    page = int(page) - 1

    df = pd.DataFrame(data)
    if geneid_filter:
        df = df.loc[df['GeneID'].str.lower().str.contains(geneid_filter.lower())]
    if degree_filter:
        df = df.loc[(df['degree'] >= degree_filter[0])&(df['degree'] <= degree_filter[1])]
    if zscore_filter:
        df = df.loc[(df['z.score'] >= zscore_filter[0])&(df['z.score'] <= zscore_filter[1])]
    if description_filter:
        df = df.loc[df['ProductDescription'].str.lower().str.contains(description_filter.lower())]
    if phase_filter:
        df = df.loc[df['phase'].isin(phase_filter)]
    
    by = [c['id'] for i, c in enumerate(table_columns) if sort_state[i] > 0]
    ascending = [not bool(s-1) for s in sort_state if s > 0]
    df = df.sort_values(by, ascending=ascending)

    data_slice = [{'index': -1-i} for i in range(page_size)]
    for i, item in enumerate(df.iloc[page*page_size:(page+1)*page_size].to_dict('records')):
        data_slice[i] = item
        item['phase'] = [
            html.Span([html.I(className="bi bi-circle-fill", style={'marginRight': '1em', 'color': phase_color_dict[item['phase']]})]),
            item['phase'],
        ]

    net_body = [
        html.Tbody([
            html.Tr([
                html.Td(item.get(c['id'], '-'), style=c['style'])
                for c in table_columns],
            # draggable='false',
            id={'type': 'net-node-table-tr', 'index': item['index']},
            style={"fontWeight": 'bold'} if item['index'] in selected_nodes else {"fontWeight": 'normal'},
            className='table-active' if item['index'] in selected_nodes else '',)
            for item in data_slice
        ])
    ]

    filtered_data_nrows = len(df)
    degree_form_message = f'Showing values between {degree_filter}'
    zscore_form_message = f'Showing values between [{zscore_filter[0]:.2f}, {zscore_filter[1]:.2f}]'

    return net_body, int(np.ceil(filtered_data_nrows / page_size)), degree_form_message, zscore_form_message


app.clientside_callback(
    """
    function save_cytoscape_png(n_clicks) {
        if(n_clicks > 0) {
            options={scale: 4, bg: "#FFFFFF"};
            saveAs(cy.png(options), "graph.png");
        }
    }
    """,
    Output("dummy-store-1", 'data'),
    Input("download-cytoscape-image-button", "n_clicks"),
)


app.clientside_callback(
    """
    function update_font_size(weight, offset, scale, apply) {
        cy.nodes().forEach(function(node, i, e) {
            size = offset + node.data('size') / 5 * scale;
            //size = 16 + 2 * scale;
            node.style('font-size', size);
            node.style('font-weight', weight);
        })
        return;
    }
    """,
    Output("dummy-store-2", 'data'),
    Input('node-label-font-weight', 'value'),
    Input('node-label-font-size', 'value'),
    # Input('label-offset-store', 'data'),
    Input('label-scale-store', 'data'),
    Input('apply-graph-settings', 'n_clicks'),
)


# @app.callback(
#     Output('label-offset-store', 'data'),
#     Input("increase-cytoscape-label-offset", "n_clicks"),
#     Input("decrease-cytoscape-label-offset", "n_clicks"),
#     State('label-offset-store', 'data'), )
# def update_sort_icons_shape(increase_n_clicks, decrease_n_clicks, offset):
#     if len(ctx.triggered) != 1:
#         raise PreventUpdate

#     if ctx.triggered[0]['prop_id'] == "increase-cytoscape-label-offset.n_clicks":
#         offset += 2

#     elif ctx.triggered[0]['prop_id'] == "decrease-cytoscape-label-offset.n_clicks":
#         if offset > 2:
#             offset -= 2

#     return offset


@app.callback(
    Output('label-scale-store', 'data'),
    Input("increase-cytoscape-label-scale", "n_clicks"),
    Input("decrease-cytoscape-label-scale", "n_clicks"),
    State('label-scale-store', 'data'), )
def update_sort_icons_shape(increase_n_clicks, decrease_n_clicks, scale):
    if len(ctx.triggered) != 1:
        raise PreventUpdate

    if ctx.triggered[0]['prop_id'] == "increase-cytoscape-label-scale.n_clicks":
        if scale >= 1:
            scale *= 1.2
        elif scale == 0:
            scale = 1.

    elif ctx.triggered[0]['prop_id'] == "decrease-cytoscape-label-scale.n_clicks":
        if scale > 1.:
            scale /= 1.2
        elif scale <= 1.:
            scale = 0

    return scale


@app.callback(
    Output("graph-settings-collapse", "is_open"),
    [Input("graph-settings-toggle-button", "n_clicks")],
    [State("graph-settings-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


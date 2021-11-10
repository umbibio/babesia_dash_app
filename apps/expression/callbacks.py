from dash.exceptions import PreventUpdate

from dash import callback_context as ctx
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db


@app.callback(
    Output('gene-dropdown', 'options'),
    Output('gene-dropdown-container', 'style'),
    Input('species-dropdown', 'value'),)
def update_gene_dropdown(species):
    if not species:
        return [], {'display': 'none'}
    
    df = db.select(
        species=species,
        table='meta_gene_all_genes',
        cols=['GeneID'])

    gene_ids = df.GeneID.tolist()
    options = [{'label': gid, 'value': gid} for gid in gene_ids]
    style = {'display': 'block'}

    return options, style


@app.callback(
    Output('2d3d-radio', 'style'),
    Input('dimred-radio', 'value'),)
def update_2d3d_visibility(dimred):

    if dimred == 'PCA':
        style = {'display': 'block'}
    else:
        style = {'display': 'none'}

    return style


@app.callback(
    Output('expression-graph', 'figure'),
    Input('species-dropdown', 'value'),
    Input('gene-dropdown', 'value'),
    Input('dimred-radio', 'value'),
    Input('2d3d-radio', 'value'),
    )
def draw_expression_plot(species, gene_id, dimred, pca_nd):

    species_triggered = ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'species-dropdown'
    
    params = dict()
    fig = go.Figure()
    scatter_function = go.Scatter

    if species is not None:
        df = db.select(
            species=species,
            table='mata_data_all_genes')

        params.update(dict(mode='markers'))
        marker_dict = dict(
            color='rgba(0., 0., 0., 0.)',
            line=dict(width=1.2, color=sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.2)')),)
        if gene_id is not None and not species_triggered:
            expression = db.select(
                species=species,
                table='expr_all_genes',
                cols=['GeneID', 'Sample', 'expr'],
                GeneID=gene_id)

            df = df.merge(expression)

            expr_colorscale = get_colorscale('Blues')

            values = df['expr'] / df['expr'].max()
            marker_expr_colors = sample_colorscale(expr_colorscale, values)
            marker_expr_colors = [c.replace('(', 'a(').replace(')', f', {v})') for c, v in zip(marker_expr_colors, values)]

            expr_colorscale = [[s, c.replace('(', 'a(').replace(')', f', {s})')] for s, c in expr_colorscale]

            marker_line_color = sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.1)')
            marker_dict = dict(
                color=marker_expr_colors,
                cmin=df['expr'].min(),
                cmax=df['expr'].max(),
                line=dict(width=1.2, color=marker_line_color),
                colorscale=expr_colorscale,
                colorbar=dict(
                    title='Expression'
                ),
            )
        params.update(dict(marker=marker_dict))

        axes_titles = dict()
        if dimred == 'PCA':
            x, y = df.loc[:, ['PC_1', 'PC_2']].values.T

            if pca_nd == '3D':
                z = df['PC_3']
                params.update(dict(z=z))
                scatter_function = go.Scatter3d
                axes_titles.update(
                    dict(scene=dict(
                        xaxis=dict(title='PC_1'),
                        yaxis=dict(title='PC_2'),
                        zaxis=dict(title='PC_3'),
                    )))
            else:
                axes_titles.update(dict( xaxis_title = 'PC_1', yaxis_title = 'PC_2', ))

        elif dimred == 'UMAP':
            x, y = df.loc[:, ['UMAP_1', 'UMAP_2']].values.T
            axes_titles.update(dict( xaxis_title = 'UMAP_1', yaxis_title = 'UMAP_2', ))

        else:
            x = y = None

        params.update(dict(x=x, y=y))

        trace = scatter_function(**params)
        fig.add_trace(trace)
        fig.update_layout(axes_titles)

    fig.update_layout({ 'yaxis': { 'scaleanchor': 'x' }, 'height': 700})
    return fig


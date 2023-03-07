from dash.exceptions import PreventUpdate

from dash import callback_context as ctx
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db


@app.callback(
    Output('expression-gene-dropdown', 'options'),
    Output('expression-gene-dropdown-container', 'style'),
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
    Input('expression-gene-dropdown', 'value'),
    Input('dimred-radio', 'value'),
    Input('2d3d-radio', 'value'),
    )
def draw_expression_plot(species, gene_id, dimred, pca_nd):

    species_triggered = ctx.triggered and ctx.triggered[0]['prop_id'] == 'species-dropdown.value'
    
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
            line=dict(width=1.2, color='rgba(0.83, 0.83, 0.83, 0.6)'),
            # line=dict(width=1.2, color=sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.2)')),
        )
        if gene_id is not None and not species_triggered:
            expression = db.select(
                species=species,
                table='expr_all_genes',
                cols=['GeneID', 'Sample', 'expr'],
                where=dict(GeneID=gene_id))

            df = df.merge(expression)

            expr_colorscale = get_colorscale('Blues')

            values = df['expr'] / df['expr'].max()
            values = values.fillna(0.)
            marker_expr_colors = sample_colorscale(expr_colorscale, values)
            marker_expr_colors_alpha = [c.replace('(', 'a(').replace(')', f', {v})') for c, v in zip(marker_expr_colors, values)]

            expr_colorscale_alpha = [[s, c.replace('(', 'a(').replace(')', f', {s})')] for s, c in expr_colorscale]

            marker_line_color_alpha = sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.1)')
            marker_dict = dict(
                color=marker_expr_colors_alpha,
                cmin=df['expr'].min(),
                cmax=df['expr'].max(),
                # line=dict(width=1.2, color=marker_line_color_alpha),
                line=dict(width=1.2, color='rgba(0.83, 0.83, 0.83, 0.6)'),
                colorscale=expr_colorscale_alpha,
                colorbar=dict(
                    title='Expression'
                ),
            )

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
                if gene_id is not None and not species_triggered:
                    marker_dict = dict(
                        color=marker_expr_colors_alpha,
                        size=3,
                        line=dict(width=1.2, color='rgba(1.0, 1.0, 1.0, 0.2)'),
                        # line=dict(width=1.2, color='rgba(0.83, 0.83, 0.83, 0.6)'),
                        # line=dict(width=1., color=sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.4)')),
                    )
                else:
                    marker_dict = dict(
                        color='rgba(0., 0., 0., 0.)',
                        size=3,
                        line=dict(width=1.2, color='rgba(1.0, 1.0, 1.0, 0.5)'),
                        # line=dict(width=1., color=sample_colorscale('Blues', [1.])[0].replace('(', 'a(').replace(')', ', 0.5)')),
                    )
            else:
                axes_titles.update(dict( xaxis_title = 'PC_1', yaxis_title = 'PC_2', ))

        elif dimred == 'UMAP':
            x, y = df.loc[:, ['UMAP_1', 'UMAP_2']].values.T
            axes_titles.update(dict( xaxis_title = 'UMAP_1', yaxis_title = 'UMAP_2', ))

        else:
            x = y = None

        params.update(dict(marker=marker_dict))
        params.update(dict(x=x, y=y))

        trace = scatter_function(**params)
        fig.add_trace(trace)
        fig.update_layout(axes_titles)

    fig.update_layout({ 'yaxis': { 'scaleanchor': 'x' }, 'height': 700})
    return fig


app.clientside_callback(
    """
    function update_gene_dropdown_value(n_clicks, species) {
        if(dash_clientside.callback_context.triggered.length == 0) return;
        prop_id = dash_clientside.callback_context.triggered[0].prop_id

        if(prop_id !== 'expression-gene-example-button.n_clicks') return;
        if(species == 'bbig') return 'BBBOND_0103330';
        if(species == 'bbov') return 'BBOV_I001860';
        if(species == 'bdiv_human') return 'Bdiv_002840c';
        if(species == 'bdiv_cow') return 'Bdiv_002840c';
        if(species == 'bmic') return 'BMR1_01G01876';
    }
    """,
    Output("expression-gene-dropdown", 'value'),
    Input("expression-gene-example-button", "n_clicks"),
    Input("species-dropdown", "value"),
)


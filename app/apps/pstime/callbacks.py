from datetime import datetime

import pandas as pd
from dash.exceptions import PreventUpdate

from dash import callback_context as ctx
from dash.dependencies import Input, Output, State, MATCH
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db
from apps.pstime.common import species_data, make_sc_plot


# app.clientside_callback(
#     """
#     function(data, layout) {
#         return {
#             'data': data,
#             'layout': layout
#         }
#     }
#     """,
#     Output({'type': 'pstime-expr-graph', 'key': MATCH}, 'figure'),
#     Input({'type': 'pstime-expr-graph-figure-data', 'key': MATCH}, 'data'),
#     Input({'type': 'pstime-expr-graph-figure-layout', 'key': MATCH}, 'data'),
# )

@app.callback(
    # Output({'type': 'pstime-expr-graph-figure-data', 'key': MATCH}, 'data'),
    # Output({'type': 'pstime-expr-graph-figure-layout', 'key': MATCH}, 'data'),
    Output({'type': 'pstime-expr-graph', 'key': MATCH}, 'figure'),
    Input('pstime-gene-dropdown', 'value'),
    State({'type': 'pstime-expr-graph', 'key': MATCH}, 'id'),
    # State({'type': 'mata-data-orth-genes', 'key': MATCH}, 'data'),
    )
def update_expression_plots(gene_id, id):
    species = id['key']

    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'pstime-gene-dropdown.value':

        fig = make_sc_plot(species, phase_visible='legendonly' if gene_id else True)
    
        if gene_id:
            # fig.update_traces(marker=dict(color='rgba(0,0,0,0)'), selector=dict(legendgrouptitle_text="Phases"))

            # df = pd.DataFrame(species_data[species])
            # df = df.merge(db.select(
            #     species=species,
            #     table='expr_orth_genes',
            #     cols=['Sample', 'expr'],
            #     where=dict(GeneID=gene_id),
            # ))
            # I forgot to include an index for the `Sample` column, which makes the following query too slow.
            # this will get fixed on next database container creation. Will need to test how fast gets compared to the method above
            df = db.select(
                species=species,
                table='mata_data_orth_genes',
                right_table='expr_orth_genes',
                right_cols=['expr'],
                right_on='Sample',
                right_where=dict(GeneID=gene_id),
            )

            expr_colorscale = get_colorscale('Blues')
            expr_colorscale_alpha = [[s, c.replace('(', 'a(').replace(')', f', {s/2})')] for s, c in expr_colorscale]
            expr_colorscale_const_alpha = [[s, c.replace('(', 'a(').replace(')', f', 0.1)')] for s, c in expr_colorscale]

            values = df['expr'] / df['expr'].max()
            marker_expr_colors = sample_colorscale(expr_colorscale, values)
            marker_expr_colors_alpha = [c.replace('(', 'a(').replace(')', f', {v/2})') for c, v in zip(marker_expr_colors, values)]



            unique_phases = df['phase'].sort_values().unique()
            colorbar_height_px = 250 - len(unique_phases) * 20
            fig.add_trace(go.Scatter(
                x=-df['PC_1'],
                y=df['PC_2'],
                mode='markers',
                marker=dict(
                    color=marker_expr_colors_alpha,
                    cmin=df['expr'].min(),
                    cmax=df['expr'].max(),
                    line=dict(width=1.2, color='rgba(0.66, 0.66, 0.66, 0.2)'),
                    # line=dict(width=1., color='rgba(0., 0., 0., 0.1)'),
                    # line=dict(width=1., color=expr_colorscale_const_alpha[6][1]),
                    colorbar=dict(
                        title="Counts",
                        len=colorbar_height_px,
                        lenmode='pixels',
                        x=1.1,
                        y=-0.1,
                        yanchor='bottom',
                    ),
                    colorscale=expr_colorscale_alpha,
                ),
                name='',
                legendgroup="expression_group",
                legendgrouptitle_text="Expression",
            ))
    else:
        raise PreventUpdate
        # fig = go.Figure(layout={ 'xaxis': {'title': 'PC_1'}, 'yaxis': {'title': 'PC_2', 'scaleanchor': 'x' }, 'height': 450, })

    return fig
    # return fig.data, fig.layout


@app.callback(
    Output({'type': 'pstime-expr-time-curve', 'key': MATCH}, 'figure'),
    Input('pstime-gene-dropdown', 'value'),
    State({'type': 'pstime-expr-time-curve', 'key': MATCH}, 'id'), )
def update_time_curve_plots(gene_id, id):
    species = id['key']

    fig = go.Figure(layout={'height': 450, "xaxis": { "visible": False }, "yaxis": { "visible": False }, 'margin': {'l':20, 'r':20, 't':60, 'b':60}})

    if species and gene_id:
        # df = pd.DataFrame(species_data[species])
        # df = df.merge(db.select(
        #     species=species,
        #     table='expr_orth_genes',
        #     cols=['Sample', 'expr'],
        #     where=dict(GeneID=gene_id),
        # ))
        # I forgot to include an index for the `Sample` column, which makes the following query too slow.
        # this will get fixed on next database container creation. Will need to test how fast gets compared to the method above
        df = db.select(
            species=species,
            table='mata_data_orth_genes',
            right_table='expr_orth_genes',
            right_cols=['expr'],
            right_on='Sample',
            right_where=dict(GeneID=gene_id),
        )

        marker_color = '#2a3f5f'.strip('#')
        # marker_color = px.colors.qualitative.Plotly[0].strip('#')
        marker_rgb = tuple(int(marker_color[i:i+2], 16) for i in (0, 2, 4))
        marker_rgba = marker_rgb + (0.2,)
        line_rgba = marker_rgb + (0.4,)

        fig.add_trace(go.Scatter(
            x=df['adj.time'],
            y=df['expr'],
            mode='markers',
            marker=dict(
                color=f'rgba{marker_rgba}',
                line=dict(width=1, color=line_rgba),
            ),
            name='Expression',
        ))
        
        df = db.select(
            species=species,
            table='spline_fit_orth_genes',
            cols=['GeneID', 't', 'expr', 'lb', 'ub'],
            where=dict(GeneID=gene_id))

        # print(df.columns)
        fig.add_trace( go.Scatter(x=df['t'], y=df['expr'], mode='lines', name='Fit'))
        fig.add_trace( go.Scatter(x=df['t'], y=df['ub'], mode='lines', line=dict(color='black', dash='dash'), name='High'))
        fig.add_trace( go.Scatter(x=df['t'], y=df['lb'], mode='lines', line=dict(color='black', dash='dash'), name='Low'))
        fig.update_layout({ "xaxis": { "visible": True }, "yaxis": { "visible": True }, })
        fig.update_layout( showlegend=False, xaxis_title = 'Time', yaxis_title = 'Expression', )
    else:
        fig.update_layout({"annotations": [
            {
                "text": "Select a gene to see expression profile.",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 16
                }
            }
        ]})

    return fig


app.clientside_callback(
    """
    function update_pstime_gene_dropdown_value(n_clicks) {
        if(dash_clientside.callback_context.triggered.length == 0) return;
        prop_id = dash_clientside.callback_context.triggered[0].prop_id

        if(prop_id !== 'pstime-gene-example-button.n_clicks') return;

        return 'Bdiv_000760c';
    }
    """,
    Output("pstime-gene-dropdown", 'value'),
    Input("pstime-gene-example-button", "n_clicks"),
)


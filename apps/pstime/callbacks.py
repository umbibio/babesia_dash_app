from dash.exceptions import PreventUpdate

from dash.dependencies import Input, Output, State, MATCH
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sample_colorscale, get_colorscale

from app import app, db


@app.callback(
    Output({'type': 'pstime-expr-graph', 'key': MATCH}, 'figure'),
    Output({'type': 'pstime-expr-graph', 'key': MATCH}, 'style'),
    Input('gene-dropdown', 'value'),
    State({'type': 'pstime-expr-graph', 'key': MATCH}, 'id'),
    State({'type': 'pstime-expr-graph', 'key': MATCH}, 'style'),)
def update_expression_plots(gene_id, id, style):
    species = id['key']

    fig = go.Figure()

    if species:
        style = {'display': 'block'}
        df = db.select(
            species=species,
            table='mata_data_orth_genes')

        unique_phases = df['phase'].sort_values().unique()
        phases_color_sequence = sample_colorscale('Rainbow', len(unique_phases))
        phases_color_sequence = [c.replace('(', 'a(').replace(')', ', 0.2)') for c in phases_color_sequence]

        for phase, color in zip(unique_phases, phases_color_sequence):
            x, y = df.loc[df['phase'] == phase, ['PC_1', 'PC_2']].values.T
            fig.add_trace(go.Scatter(
                x=x,
                y=y,
                mode='markers',
                marker=dict(
                    color=color if not gene_id else 'rgba(0., 0., 0., 0.)',
                    line=dict(width=0.8, color=color),
                ),
                name=phase,
                legendgroup="phases_group",
                legendgrouptitle_text="Phases",
            ))

        x, y = df.loc[df['cell.ord']-1, ['sc1', 'sc2']].values.T
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='lines',
            line=dict(color='Black', width=1),
            name='Timeline',
            legendgroup="timeline_group",
            legendgrouptitle_text="Timeline",
        ))

        x, y = df.loc[df['adj.time'] == df['adj.time'].min(), ['sc1', 'sc2']].values.T
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(color='Black', size=20),
            opacity=0.8,
            name='Time Start',
            legendgroup="timeline_group",
            legendgrouptitle_text="Timeline",
        ))

        if gene_id:
            expression = db.select(
                species=species,
                table='expr_orth_genes',
                cols=['GeneID', 'Sample', 'expr'],
                GeneID=gene_id)

            df = df.merge(expression)

            expr_colorscale = get_colorscale('Blues')

            values = df['expr'] / df['expr'].max()
            marker_expr_colors = sample_colorscale(expr_colorscale, values)
            marker_expr_colors = [c.replace('(', 'a(').replace(')', f', {v/2})') for c, v in zip(marker_expr_colors, values)]

            expr_colorscale = [[s, c.replace('(', 'a(').replace(')', f', {s/2})')] for s, c in expr_colorscale]

            colorbar_height_px = 250 - len(unique_phases) * 20
            fig.add_trace(go.Scatter(
                x=df['PC_1'],
                y=df['PC_2'],
                mode='markers',
                marker=dict(
                    color=marker_expr_colors,
                    cmin=df['expr'].min(),
                    cmax=df['expr'].max(),
                    line=dict(width=0., color='rgba(0., 0., 0., 0.)'),
                    colorbar=dict(
                        title="Counts",
                        len=colorbar_height_px,
                        lenmode='pixels',
                        x=1.1,
                        y=0.,
                        yanchor='bottom',
                    ),
                    colorscale=expr_colorscale,
                ),
                name='',
                legendgroup="expression_group",
                legendgrouptitle_text="Expression",
            ))
        


    fig.update_layout(
        { 'yaxis': { 'scaleanchor': 'x' }, 'height': 500, },
        xaxis_title = 'PC_1',
        yaxis_title = 'PC_2',
    )

    return fig, style


@app.callback(
    Output({'type': 'pstime-expr-time-curve', 'key': MATCH}, 'figure'),
    Output({'type': 'pstime-expr-time-curve', 'key': MATCH}, 'style'),
    Input('gene-dropdown', 'value'),
    State({'type': 'pstime-expr-time-curve', 'key': MATCH}, 'id'), )
def update_time_curve_plots(gene_id, id):
    species = id['key']

    fig = go.Figure()

    if species and gene_id:
        style = {'display': 'block'}
        df = db.select(
            species=species,
            table='mata_data_orth_genes')

        expression = db.select(
            species=species,
            table='expr_orth_genes',
            cols=['GeneID', 'Sample', 'expr'],
            GeneID=gene_id)

        marker_color = '#2a3f5f'.strip('#')
        # marker_color = px.colors.qualitative.Plotly[0].strip('#')
        marker_rgb = tuple(int(marker_color[i:i+2], 16) for i in (0, 2, 4))
        marker_rgba = marker_rgb + (0.2,)
        line_rgba = marker_rgb + (0.4,)

        df = df.merge(expression)
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
            GeneID=gene_id)

        fig.add_trace( go.Scatter(x=df['t'], y=df['expr'], mode='lines', name='Fit'))
        fig.add_trace( go.Scatter(x=df['t'], y=df['ub'], mode='lines', line=dict(color='black', dash='dash'), name='High'))
        fig.add_trace( go.Scatter(x=df['t'], y=df['lb'], mode='lines', line=dict(color='black', dash='dash'), name='Low'))
    else:
        style = {'display': 'none'}

    fig.update_layout(
        {'height': 500},
        showlegend=False,
        xaxis_title = 'Time',
        yaxis_title = 'Expression',
    )

    return fig, style


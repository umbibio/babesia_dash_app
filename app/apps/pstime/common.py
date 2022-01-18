import pandas as pd
import plotly.graph_objects as go

from plotly.colors import sample_colorscale, get_colorscale

from app import db
from data import species_keys, species_names

species_data = { key: db.select( species=key, table='mata_data_orth_genes').to_dict() for key in species_keys if key != 'bmic'}

phase_abbrv = ['G', 'SM', 'MC', 'C', 'NA']
phase_names = ['G', 'SM', 'MC', 'C', 'Not Available']
phase_colors = ["#1A5878", "#C44237", "#AD8941", "#E99093", "#D3D3D3", "#FFFFFF", "#50594B"]
phase_colors_rgb = ["rgb(26, 88, 120)", "rgb(196, 66, 55)", "rgb(173, 137, 65)", "rgb(233, 144, 147)", "rgb(211, 211, 211)", "rgb(255, 255, 255)", "rgb(80, 89, 75)"]
phase_color_dict = dict(zip(phase_abbrv, phase_colors))
phase_color_rgb_dict = dict(zip(phase_abbrv, phase_colors_rgb))


# phases_color_sequence = sample_colorscale('Rainbow', 7)
phases_color_sequence = [c.replace('(', 'a(').replace(')', ', 0.2)') for c in phase_colors_rgb]

def make_sc_plot(species, phase_visible=True):
    fig = go.Figure(layout={ 'xaxis': {'title': 'PC_1'}, 'yaxis': {'title': 'PC_2', 'scaleanchor': 'x' }, 'height': 450, 'margin': {'l':10, 'r':10, 't':60, 'b':60}})
    

    df = pd.DataFrame(species_data[species])
    unique_phases = df['phase'].sort_values().unique()
    unique_phases = ['G', 'SM', 'MC', 'C']
    for phase, color in zip(unique_phases, phases_color_sequence):
        x, y = df.loc[df['phase'] == phase, ['PC_1', 'PC_2']].values.T
        x = -x
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(
                color=color,
                line=dict(width=0.8, color=color),
            ),
            name=phase,
            visible=phase_visible,
            legendgroup="phases_group",
            legendgrouptitle_text="Phases",
        ))

    x, y = df.loc[df['cell.ord']-1, ['sc1', 'sc2']].values.T
    x = -x
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
    x = -x
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

    return fig


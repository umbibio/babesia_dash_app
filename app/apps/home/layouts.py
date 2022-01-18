from dash import dcc
from dash import html

import dash_bootstrap_components as dbc

menu = None

body = [
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H2("Babesia Single Cell Atlas")),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(dcc.Markdown('''
The Babesia Single Cell atlas provides an interactive app to explore gene
expression at the single cell resolution during the intra-erythrocytic
development cycle from several Babesia species. To explore the data click
on one of the tabs above.

1. **Expression**: Explore expression of genes across thousands of asynchronously dividing single cells projected on PCA or UMAP coordinates.
2. **Pseudo-time**: Time-course reconstruction of gene expression during Babesia cell cycle. Includes orthologous genes with pseudo-time correlating expression profiles.
3. **Network**: Co-expression network of orthologous genes.

''')),
                dbc.Col(
                    dbc.Carousel(items=[
                        {"key": "1", "src": "/babesiasc/assets/newplot-expression.png"},
                        {"key": "2", "src": "/babesiasc/assets/newplot-pstime.png"},
                        {"key": "3", "src": "/babesiasc/assets/network-graph.png"},
                    ], interval=5000, className="carousel-fade", indicators=False)
                )])),
        ],),
    ), class_name="mb-4 mt-4"),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Citation")),
            dbc.CardBody(dcc.Markdown('''
Yasaman Rezvani*, Caroline D Keroack*, Brendan Elsworth, Argenis Arriojas, Marc-Jan Gubbels, Manoj T Duraisingh, Kourosh Zarringhalam, "Single cell transcriptional atlas of Babesia species reveals coordinated progression of transcriptomes and identifies conserved and species-specific transcriptional profiles", 2022, BioRxiv
''')),
        ],),),
        dbc.Col(dbc.Card([
            dbc.CardHeader(html.H4("Contact")),
            dbc.CardBody(dcc.Markdown('''
For questions or comments please contact:

Kourosh.Zarringhalam at umb dot edu
''')),
        ],),),
    ]),
]


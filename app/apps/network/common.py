table_columns=[
    {'name':             'Gene ID', 'id':             'GeneID', 'type':    'alpha', 'header_style': {'width': '10%', 'minWidth': '140px'}, 'style': {'width': '10%', 'minWidth': '140px'}},
    {'name':                 'Deg', 'id':             'degree', 'type': 'numeric', 'header_style': {'width':  '8%', 'minWidth':  '92px'}, 'style': {'width':  '8%', 'minWidth':  '92px', 'textAlign': 'right'}},
    {'name':                'ZVal', 'id':            'z.score', 'type': 'numeric', 'header_style': {'width':  '8%', 'minWidth':  '92px'}, 'style': {'width':  '8%', 'minWidth':  '92px', 'textAlign': 'right'}},
    {'name': 'Product Description', 'id': 'ProductDescription', 'type':    'alpha', 'header_style': {}, 'style': {}},
    {'name':               'Phase', 'id':              'phase', 'type':    'alpha', 'header_style': {'width': '10%', 'minWidth':  '90px'}, 'style': {'width': '10%', 'minWidth':  '90px'}},
]


phase_abbrv = ['G', 'SM', 'MC', 'C', 'NA']
phase_names = ['G', 'SM', 'MC', 'C', 'Not Available']
phase_colors = ["#1A5878", "#C44237", "#AD8941", "#E99093", "#D3D3D3", "#FFFFFF", "#50594B"]
phase_color_dict = dict(zip(phase_abbrv, phase_colors))

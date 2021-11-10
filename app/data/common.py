import os

data_path = os.environ.get('BSCAPP_DATA_PATH')
data_path = './data/tsv_files' if data_path is None else data_path

species_keys = [
    'bbig',
    'bbov',
    'bdiv_human',
    'bdiv_cow',
    'bmic',
]


species_names = {
    'bbig': 'Babesia Bigemina',
    'bbov': 'Babesia Bovis',
    'bdiv_human': 'Babesia Divergens in human cell host',
    'bdiv_cow': 'Babesia Divergens in cow cell host',
    'bmic': 'Babesia microti',
}


table_names = [
    'expr_all_genes',
    'expr_orth_genes',
    'meta_gene_all_genes',
    'meta_gene_orth_genes',
    'mata_data_all_genes',
    'mata_data_orth_genes',
    'spline_fit_orth_genes',
]


species_tables = {
    'expr_all_genes': [
        {'name': 'GeneID', 'dtype': str},
        {'name': 'Sample', 'dtype': str},
        {'name': 'expr', 'dtype': float},
    ],
    'expr_orth_genes': [
        {'name': 'GeneID', 'dtype': str},
        {'name': 'Sample', 'dtype': str},
        {'name': 'expr', 'dtype': float},
    ],
    'meta_gene_all_genes': [
        {'name': 'GeneID', 'dtype': str},
    ],
    'meta_gene_orth_genes': [
        {'name': 'GeneID', 'dtype': str},
    ],
    'mata_data_all_genes': [
        {'name': 'Sample', 'dtype': str},
        {'name': 'seurat_clusters', 'dtype': str},
        {'name': 'PC_1', 'dtype': float},
        {'name': 'PC_2', 'dtype': float},
        {'name': 'PC_3', 'dtype': float},
        {'name': 'UMAP_1', 'dtype': float},
        {'name': 'UMAP_2', 'dtype': float},
    ],
    'mata_data_orth_genes': [
        {'name': 'Sample', 'dtype': str},
        {'name': 'pt', 'dtype': float},
        {'name': 't', 'dtype': float},
        {'name': 'adj.time', 'dtype': float},
        {'name': 'adj.time.idx', 'dtype': int},
        {'name': 'sc1', 'dtype': float},
        {'name': 'sc2', 'dtype': float},
        {'name': 'rep', 'dtype': int},
        {'name': 'spp', 'dtype': str},
        {'name': 'cell.ord', 'dtype': int},
        {'name': 'PC_1', 'dtype': float},
        {'name': 'PC_2', 'dtype': float},
        {'name': 'PC_3', 'dtype': float},
        {'name': 'UMAP_1', 'dtype': float},
        {'name': 'UMAP_2', 'dtype': float},
        {'name': 'phase', 'dtype': str},
    ],
    'spline_fit_orth_genes': [
        {'name': 'GeneID', 'dtype': str},
        {'name': 't', 'dtype': float},
        {'name': 'expr', 'dtype': float},
        {'name': 'lb', 'dtype': float},
        {'name': 'ub', 'dtype': float},
    ],
}

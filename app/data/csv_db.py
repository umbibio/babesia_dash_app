# This db will read from a csv file for each query
import os
import pandas as pd

from data import data_path


tables_cache = {}


def select(species, table, cols=None, offset=None, nrows=None, force_read=False, **kvargs):
    table_filename = f'{species}_{table}.tsv'
    table_path = os.path.join(data_path, table_filename)

    if force_read:
        df = pd.read_csv(table_path, sep='\t', skiprows=offset, nrows=nrows)

    else:
        if not table_filename in tables_cache.keys():
            # print(f'+++ start fetching {table_filename} ... reading file ...')
            tables_cache[table_filename] = pd.read_csv(table_path, sep='\t')
        else:
            # print(f'+++ start fetching {table_filename} ... using cache ...')
            pass

        end = nrows if offset is None else (None if nrows is None else offset+nrows)
        df = tables_cache[table_filename].iloc[offset:end]

    for column, value in kvargs.items():
        if type(value) == list:
            df = df.loc[df[column].isin(value)]
        else:
            df = df.loc[df[column] == value]

    if cols is not None:
        df = df.loc[:, cols]

    # print(f'--- done fetching {table_filename}')
    return df


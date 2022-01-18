#!/usr/bin/env python

import os
from glob import glob
import numpy as np
import pandas as pd


TSV_FILES = glob(os.path.join('data', 'tsv_files', '*.tsv'))
TSV_FILES.sort()


def get_sql_datatype(series):
    print(series.name, flush=True, end=', ')

    if series.name.lower() == 'phase':
        # force str for phase. If first element is 'NA' then we wrongly infer float
        dtype = str
    else:
        # infer type from first element value
        dtype = type(series.iat[0])

    if dtype == str:
        max_length = series.str.len().max()
        return f'VARCHAR ({int(max_length)})'
    elif dtype in [int, np.int64]:
        return 'INT'
    elif dtype in [float, np.float64]:
        return 'FLOAT'
    else:
        raise ValueError(f"Don't know how to translate dtype {dtype}")


def generate_create_tables():
    print('Generating sql files for table creation...')
    CREATE_TABLE_TEMPLATE = "CREATE TABLE {table_name} ( {columns_specs} );\n"
    OUTPUT_FILE = os.path.join('data', 'initdb.d', '01_create_tables.sql')

    with open(OUTPUT_FILE, 'w') as file:

        for table_path in TSV_FILES:
            print(f'\tProcessing {table_path} with columns:', flush=True, end=' ')
            table_filename = os.path.basename(table_path)
            table_name = os.path.splitext(table_filename)[0]
            
            df = pd.read_csv(table_path, sep='\t')
            columns_specs = ', '.join([' '.join([f"`{cn}`", get_sql_datatype(df[cn])]) for cn in df.columns])
            line = CREATE_TABLE_TEMPLATE.format(table_name=table_name, columns_specs=columns_specs)
            file.write(line)
            print(flush=True)


def generate_create_indices():
    print('Generating sql files for index creation...')

    CREATE_INDEX_TEMPLATE = "CREATE INDEX {index_name} ON {table_name} ( {columns} );\n"
    CREATE_UNIQUE_INDEX_TEMPLATE = "CREATE UNIQUE INDEX {index_name} ON {table_name} ( {columns} );\n"
    OUTPUT_FILE = os.path.join('data', 'initdb.d', '02_create_indices.sql')

    with open(OUTPUT_FILE, 'w') as file:

        for table_path in TSV_FILES:
            print(f'\tProcessing {table_path}...')

            table_filename = os.path.basename(table_path)
            table_name = os.path.splitext(table_filename)[0]
            
            df = pd.read_csv(table_path, sep='\t', nrows=5)

            column_list = [cn for cn in df.columns if cn in ['GeneID', 'Sample', 't']]
            if column_list:
                TEMPLATE = CREATE_INDEX_TEMPLATE if len(column_list) == 2 else CREATE_UNIQUE_INDEX_TEMPLATE

                for column in column_list:
                    if column == 't':
                        continue
                    index_name = f"index_{table_name}_{column}"
                    line = TEMPLATE.format(index_name=index_name, table_name=table_name, columns=column)
                    file.write(line)
            else:
                column_list = [cn for cn in df.columns if cn in ['src', 'trg']]
                if len(column_list) == 2:
                    index_name = f"index_{table_name}_" + '_'.join(column_list)
                    line = CREATE_UNIQUE_INDEX_TEMPLATE.format(index_name=index_name, table_name=table_name, columns=', '.join(column_list))
                    file.write(line)
                    column = column_list[1]
                    index_name = f"index_{table_name}_{column}"
                    line = CREATE_INDEX_TEMPLATE.format(index_name=index_name, table_name=table_name, columns=column)
                    file.write(line)
                else:
                    print(table_path)
                    print(column_list)
                    raise NotImplementedError


def generate_insert_data():
    print('Generating sql files for data loading...')
    INSERT_DATA_TEMPLATE = "LOAD DATA INFILE '{table_path}' INTO TABLE {table_name} FIELDS TERMINATED BY '\\t' IGNORE 1 LINES;\n"
    OUTPUT_FILE_TEMPLATE = os.path.join('data', 'initdb.d', '03_insert_data_into_{table_name}.sql')


    for table_path in TSV_FILES:
        print(f'\tProcessing {table_path}...')
        table_path = os.path.join('/app', table_path)
        table_filename = os.path.basename(table_path)
        table_name = os.path.splitext(table_filename)[0]

        with open(OUTPUT_FILE_TEMPLATE.format(table_name=table_name), 'w') as file:
            line = INSERT_DATA_TEMPLATE.format(table_path=table_path, table_name=table_name)
            file.write(line)

def main():
    generate_create_tables()
    generate_create_indices()
    generate_insert_data()

if __name__ == "__main__":
    main()

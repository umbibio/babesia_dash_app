import os
import pandas as pd
import mysql.connector


connection_params = {n: os.environ.get(f'MARIADB_{n.upper()}') for n in ['host', 'user', 'password', 'database']}

cnx = mysql.connector.connect(**connection_params)


def select(species, table, cols=None, offset=None, nrows=None, force_read=False, **kvargs):
    cursor = cnx.cursor(dictionary=True)

    columns_str = '*' if cols is None else ', '.join([f"`{c}`" for c in cols])
    table_name = f'{species}_{table}'
    # print(f'+++ start fetching {table_name} ...')

    where_str = 'WHERE ' if len(kvargs) > 0 else ''
    where_str += 'AND '.join([f"`{k}`='{v}' " for k, v in kvargs.items()])

    query = f"SELECT {columns_str} FROM {table_name} {where_str};"
    # print(query)

    cursor.execute(query)

    data = list(cursor)

    df = pd.DataFrame(data)

    cursor.close()
    # print(f'--- done fetching {table_name}')
    return df


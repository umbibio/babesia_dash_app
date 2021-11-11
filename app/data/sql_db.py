import atexit
import os
import pandas as pd
from mysql.connector.pooling import MySQLConnectionPool


class DBPool(object):
    def __init__(self) -> None:
        dbconfig = {n: os.environ.get(f'MARIADB_{n.upper()}') for n in ['host', 'user', 'password', 'database']}
        self.pool = MySQLConnectionPool(pool_name="bsc_pool", pool_size = 5, **dbconfig)

    def get_table_from_query(self, query):
        cnx = self.pool.get_connection()
        cursor = cnx.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        cursor.close()

        data = list(cursor)
        df = pd.DataFrame(data)

        cnx.close()
        return df
    
    def close(self):
        print(f'closing db pool: {self.pool._remove_connections()} connections closed.')


conn = DBPool()
atexit.register(conn.close)


def select(species, table, cols=None, offset=None, nrows=None, force_read=False, **kvargs):

    columns_str = '*' if cols is None else ', '.join([f"`{c}`" for c in cols])
    table_name = f'{species}_{table}'
    # print(f'+++ start fetching {table_name} ...')

    or_groups = []
    for col, val in kvargs.items():
        if type(val) == list:
            conditions = ' OR '.join([f"`{col}`='{v}'" for v in val])
        else:
            conditions = f"`{col}`='{val}'"
        or_groups.append(f"({conditions})")
    
    combined_conditions = ' AND '.join(or_groups)
    if combined_conditions:
        where_str = f"WHERE {combined_conditions}"
    else:
        where_str = ''

    query = f"SELECT {columns_str} FROM {table_name} {where_str};"
    # print(query)

    df = conn.get_table_from_query(query)

    # print(f'--- done fetching {table_name}')
    return df


from typing import List, Dict, Union
import atexit
import os
import pandas as pd
from mysql.connector.pooling import MySQLConnectionPool


class DBPool(object):
    def __init__(self) -> None:
        dbconfig = {n: os.environ.get(f'MARIADB_{n.upper()}') for n in ['host', 'user', 'password', 'database']}
        self.pool = MySQLConnectionPool(pool_name="bsc_pool", pool_size = 32, **dbconfig)

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


# TODO: Figure a way to make table joins. Maybe a new, separate method would suffice
# Here's something to start with
def join(species, left, right, ):
    pass

def select(species:     str,
           table:       str,
           cols:        List[str]=[],
           where:       Dict[str, Union[str, List[str]]]={},
           right_table: str='',
           right_cols:  List[str]=[],
           right_on:    str='',
           right_where: Dict[str, Union[str, List[str]]]={},) -> pd.DataFrame:

    table_name = f'{species}_{table}'
    cols = [f"`{table_name}`.`{c}`" for c in cols] if cols else [f"`{table_name}`.*"]

    if right_table:
        right_table_name = f'{species}_{right_table}'
        right_cols = [f"`{right_table_name}`.`{c}`" for c in right_cols] if right_cols else [f"`{right_table_name}`.*"]
        cols.extend(right_cols)

        assert right_on != ''
        table_str = f'`{table_name}` LEFT JOIN `{right_table_name}` ON `{table_name}`.`{right_on}` = `{right_table_name}`.`{right_on}`'
    else:
        table_str = f'`{table_name}`'

    columns_str = ', '.join(cols)
    # print(f'+++ start fetching {table_name} ...')

    or_groups = []
    for col, val in where.items():
        if type(val) == list:
            conditions = ' OR '.join([f"`{table_name}`.`{col}`='{v}'" for v in val])
        else:
            conditions = f"`{table_name}`.`{col}`='{val}'"
        if val:
            or_groups.append(f"({conditions})")

    for col, val in right_where.items():
        if type(val) == list:
            conditions = ' OR '.join([f"`{right_table_name}`.`{col}`='{v}'" for v in val])
        else:
            conditions = f"`{right_table_name}`.`{col}`='{val}'"
        if val:
            or_groups.append(f"({conditions})")
    
    combined_conditions = ' AND '.join(or_groups)
    if combined_conditions:
        where_str = f"WHERE {combined_conditions}"
    else:
        where_str = ''

    query = f"SELECT {columns_str} FROM {table_str} {where_str};"
    # print(query)

    df = conn.get_table_from_query(query)

    # print(f'--- done fetching {table_name}')
    return df


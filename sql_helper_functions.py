from dataclasses import fields
from textwrap import dedent

from spotify_helper_functions import Song


def construct_create_table_query(table_name: str, fields: str) -> str:
    query: str = dedent(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
        \t{fields}
        );
    """)
    print(f"create table query:\n{query}")
    return query


def construct_truncate_table_query(table_name: str) -> str:
    query = f"TRUNCATE TABLE {table_name}"
    print(f"truncate table query:\n{query}")
    return query


def construct_insert_data_query(table_name: str, temp_table_name: str) -> str:
    columns = ", ".join([field.name for field in fields(Song)])
    query = f"""
        INSERT INTO {table_name} ({columns})
        SELECT {columns}
        FROM {temp_table_name}
    """
    print(f"insert data query:\n{query}")
    return query


def construct_drop_table_query(table_name: str) -> str:
    query = f"DROP TABLE IF EXISTS {table_name}"
    print(f"drop table query: {query}")
    return query

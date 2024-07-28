from dataclasses import dataclass, fields
from textwrap import dedent
from snowflake.connector.cursor import SnowflakeCursor

from spotify_helper_functions import Song


@dataclass
class SnowflakeConfig:
    user: str
    password: str
    account: str
    warehouse: str
    database: str
    schema: str


def create_and_use_snowflake_warehouse(config: SnowflakeConfig, cursor: SnowflakeCursor) -> None:
    # Create a warehouse
    cursor.execute(f"CREATE WAREHOUSE IF NOT EXISTS {config.warehouse}")

    # Use the warehouse
    cursor.execute(f"USE WAREHOUSE {config.warehouse}")


def create_and_use_snowflake_database(config: SnowflakeConfig, cursor: SnowflakeCursor) -> None:
    # Create a database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.database}")

    # Use the database
    cursor.execute(f"USE DATABASE {config.database}")


def create_and_use_snowflake_schema(config: SnowflakeConfig, cursor: SnowflakeCursor) -> None:
    # Create a schema
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {config.schema}")

    # Use the schema
    cursor.execute(f"USE SCHEMA {config.schema}")


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

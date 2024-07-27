import os
from typing import List, Dict
from dataclasses import dataclass, fields
from textwrap import dedent
import snowflake.connector
from snowflake.connector import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor

from get_recommended_songs import Song


@dataclass
class SnowflakeConfig:
    user: str
    password: str
    account: str
    warehouse: str
    database: str
    schema: str


PYTHON_TO_SQL_TYPE_MAPPING: Dict[type, str] = {
    str: "VARCHAR(255)",
    int: "INT",
    List[str]: "TEXT",
}

if __name__ == "__main__":
    # Configure Snowflake parameters
    config = SnowflakeConfig(
        user=os.environ["SNOWFLAKE_USERNAME"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse="recommended_songs_warehouse",
        database="recommended_songs_database",
        schema="recommended_songs_schema",
    )
    
    # Establish a connection
    connection: SnowflakeConnection = snowflake.connector.connect(
        user=config.user,
        password=config.password,
        account=config.account,
        warehouse=config.warehouse,
        database=config.database,
        schema=config.schema,
    )

    # Create a cursor object
    cursor: SnowflakeCursor = connection.cursor()

    # Create a database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.database}")

    # Create a schema
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {config.schema}")

    # Use the database and schema
    cursor.execute(f"USE DATABASE {config.database}")
    cursor.execute(f"USE SCHEMA {config.schema}")

    # Create a table
    for field in fields(Song):
        print(f"{field.name} {field.type}")
    fields_list: str = ",\n\t".join(
        f"{field.name} {PYTHON_TO_SQL_TYPE_MAPPING[field.type]}" for field in fields(Song)
    )
    print(f"fields list: {fields_list}")
    create_table_query: str = dedent(f"""
    CREATE TABLE IF NOT EXISTS Songs (
    \t{fields_list}
    );
    """)
    print(f"create_table_query:\n{create_table_query}")
    cursor.execute(create_table_query)
    print("Table created successfully.")

    # Commit the transaction
    connection.commit()

    # Close the cursor and connection
    cursor.close()
    connection.close()

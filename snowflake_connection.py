import os
from typing import List, Dict
from dataclasses import dataclass, fields
from pandas import DataFrame
import snowflake.connector
from snowflake.connector import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor
from snowflake.connector.pandas_tools import write_pandas

from spotify_helper_functions import (
    Song,
    SPOTIFY_API_CLIENT,
    SEED_ARTISTS,
    get_recommended_songs_based_on_artists,
    construct_recommended_songs_dataframe,
)
from sql_helper_functions import (
    construct_create_table_query,
    construct_truncate_table_query,
    construct_insert_data_query,
    construct_drop_table_query,
)


@dataclass
class SnowflakeConfig:
    user: str
    password: str
    account: str
    warehouse: str
    database: str
    schema: str


TABLE_NAME: str = "RECOMMENDED_SONGS"  # The names are in uppercase in order to avoid the `Table does not exist` SQL compilation error
TEMP_TABLE_NAME: str = "TEMP_RECOMMENDED_SONGS"
SCHEMA_NAME: str = "RECOMMENDED_SONGS_SCHEMA"
DATABASE_NAME: str = "RECOMMENDED_SONGS_DATABASE"


PYTHON_TO_SQL_TYPE_MAPPING: Dict[type, str] = {
    str: "VARCHAR(255)",
    int: "INT",
    List[str]: "TEXT",
}


def create_snowflake_objects(config: SnowflakeConfig, cursor: SnowflakeCursor) -> None:
    # Create a warehouse
    cursor.execute(f"CREATE WAREHOUSE IF NOT EXISTS {config.warehouse}")

    # Create a database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.database}")

    # Create a schema
    cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {config.schema}")

    # Use the database and schema
    cursor.execute(f"USE DATABASE {config.database}")
    cursor.execute(f"USE SCHEMA {config.schema}")
    cursor.execute(f"USE WAREHOUSE {config.warehouse}")


if __name__ == "__main__":
    # Configure Snowflake parameters
    snowflake_config = SnowflakeConfig(
        user=os.environ["SNOWFLAKE_USERNAME"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse="RECOMMENDED_SONGS_WAREHOUSE",
        database=DATABASE_NAME,
        schema=SCHEMA_NAME,
    )

    # Establish a connection
    snowflake_connection: SnowflakeConnection = snowflake.connector.connect(
        user=snowflake_config.user,
        password=snowflake_config.password,
        account=snowflake_config.account,
        warehouse=snowflake_config.warehouse,
        database=snowflake_config.database,
        schema=snowflake_config.schema,
    )

    # Create a cursor object
    snowflake_cursor: SnowflakeCursor = snowflake_connection.cursor()

    # Use the cursor to object to create a database and a schema
    create_snowflake_objects(config=snowflake_config, cursor=snowflake_cursor)

    # Define columns for a Snowflake table
    for field in fields(Song):
        print(f"{field.name} {field.type}")
    fields_str: str = ",\n\t".join(
        f"{field.name} {PYTHON_TO_SQL_TYPE_MAPPING[field.type]}" for field in fields(Song)
    )
    print(f"fields list: {fields_str}")

    # Create the table
    create_table_query: str = construct_create_table_query(table_name=TABLE_NAME, fields=fields_str)
    snowflake_cursor.execute(create_table_query)
    print(f"Table `{TABLE_NAME}` created successfully.")

    # Retrieve recommended songs from Spotify Web API
    recommended_songs: List[Dict] = get_recommended_songs_based_on_artists(
        api_client=SPOTIFY_API_CLIENT,
        seed_artists=list(SEED_ARTISTS.values()),
        recommendation_size=10,
    )
    recommended_songs_dataframe: DataFrame = construct_recommended_songs_dataframe(recommended_songs=recommended_songs)

    # Upsert Spotify recommended songs to the table
    create_temp_table_query: str = construct_create_table_query(table_name=TEMP_TABLE_NAME, fields=fields_str)
    snowflake_cursor.execute(create_temp_table_query)
    print(f"Table `{TEMP_TABLE_NAME}` created successfully.")

    write_pandas(
        conn=snowflake_connection,
        df=recommended_songs_dataframe,
        table_name=TEMP_TABLE_NAME,
        schema=SCHEMA_NAME,
        database=DATABASE_NAME,
    )
    truncate_table_query: str = construct_truncate_table_query(table_name=TABLE_NAME)
    snowflake_cursor.execute(truncate_table_query)

    insert_data_query: str = construct_insert_data_query(table_name=TABLE_NAME, temp_table_name=TEMP_TABLE_NAME)
    snowflake_cursor.execute(insert_data_query)

    drop_temp_table_query: str = construct_drop_table_query(table_name=TEMP_TABLE_NAME)
    snowflake_cursor.execute(drop_temp_table_query)

    # Commit the transaction
    snowflake_connection.commit()

    # Close the cursor and connection
    snowflake_cursor.close()
    snowflake_connection.close()

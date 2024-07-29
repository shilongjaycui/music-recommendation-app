import sys
import os
from typing import List, Dict
from dataclasses import fields
import streamlit as st
import snowflake.connector
from snowflake.connector import SnowflakeConnection
from snowflake.connector.cursor import SnowflakeCursor
from snowflake.connector.pandas_tools import write_pandas

# Get the directory of the current file
current_dir = os.path.dirname(__file__)
# Get the parent directory
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
# Add the parent directory to sys.path
sys.path.append(parent_dir)

from src.sql_helper_functions import (
    SnowflakeConfig,
    create_and_use_snowflake_warehouse,
    create_and_use_snowflake_database,
    create_and_use_snowflake_schema,
    construct_create_table_query,
    construct_truncate_table_query,
    construct_insert_data_query,
    construct_drop_table_query,
)
from src.spotify_helper_functions import (
    Artist,
    Song,
    SPOTIFY_API_CLIENT,
    SEED_ARTISTS,
    get_several_artists,
    get_recommended_songs_based_on_artists,
    construct_recommended_songs_dataframe,
)


TABLE_NAME: str = "RECOMMENDED_SONGS"  # The names are in uppercase in order to avoid the `Table does not exist` SQL compilation error
TEMP_TABLE_NAME: str = "TEMP_RECOMMENDED_SONGS"
SCHEMA_NAME: str = "RECOMMENDED_SONGS_SCHEMA"
DATABASE_NAME: str = "RECOMMENDED_SONGS_DATABASE"
PYTHON_TO_SQL_TYPE_MAPPING: Dict[type, str] = {
    str: "VARCHAR(255)",
    int: "INT",
    List[str]: "TEXT",
}


def display_artist(artist: Artist):
    st.image(artist.artist_image_url, use_column_width=True)
    st.markdown(f"### {artist.artist_name}")
    st.markdown(", ".join(artist.artist_genres))


# Initialize session state for recommended songs DataFrame if not already set
if 'recommended_songs_dataframe' not in st.session_state:
    st.session_state['recommended_songs_dataframe'] = None

# Artists Section
st.title("Artists")
artists: List[Artist] = get_several_artists(
    api_client=SPOTIFY_API_CLIENT,
    spotify_urls=list(SEED_ARTISTS.values()),
)
# Create columns for artists
cols = st.columns([2 for _ in artists])
# Display each artist in a column
for col, artist in zip(cols, artists):
    with col:
        display_artist(artist)
if st.button('Get recommended songs'):
    recommended_songs: List[Dict] = get_recommended_songs_based_on_artists(
        api_client=SPOTIFY_API_CLIENT,
        seed_artists=list(SEED_ARTISTS.values()),
        recommendation_size=10,
    )
    st.session_state['recommended_songs_dataframe'] = construct_recommended_songs_dataframe(recommended_songs=recommended_songs)

# Display the DataFrame if it exists in session state
if st.session_state['recommended_songs_dataframe'] is not None:
    st.dataframe(st.session_state['recommended_songs_dataframe'])

    # Button to save recommended songs to Snowflake
    if st.button('Save recommended songs to Snowflake'):
        # Configure Snowflake parameters
        snowflake_config = SnowflakeConfig(
            user=os.environ["SNOWFLAKE_USERNAME"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            warehouse="RECOMMENDED_SONGS_WAREHOUSE",
            database=DATABASE_NAME,
            schema=SCHEMA_NAME,
        )
        # Establish a connection to Snowflake
        snowflake_connection: SnowflakeConnection = snowflake.connector.connect(
            user=snowflake_config.user,
            password=snowflake_config.password,
            account=snowflake_config.account,
            warehouse=snowflake_config.warehouse,
            database=snowflake_config.database,
            schema=snowflake_config.schema,
        )

        # Create a Snowflake cursor object
        snowflake_cursor: SnowflakeCursor = snowflake_connection.cursor()

        # Create and use Snowflake warehouse, database, schema
        create_and_use_snowflake_warehouse(config=snowflake_config, cursor=snowflake_cursor)
        create_and_use_snowflake_database(config=snowflake_config, cursor=snowflake_cursor)
        create_and_use_snowflake_schema(config=snowflake_config, cursor=snowflake_cursor)

        # Define columns for a Snowflake table
        fields_str: str = ",\n\t".join(
            f"{field.name} {PYTHON_TO_SQL_TYPE_MAPPING[field.type]}" for field in fields(Song)
        )

        # Create the table
        create_table_query: str = construct_create_table_query(table_name=TABLE_NAME, fields=fields_str)
        snowflake_cursor.execute(create_table_query)
        st.write(f"(Step 1 of 6) Created the `{TABLE_NAME}` Snowflake table.")

        # Upsert Spotify recommended songs to the table
        create_temp_table_query: str = construct_create_table_query(table_name=TEMP_TABLE_NAME, fields=fields_str)
        snowflake_cursor.execute(create_temp_table_query)
        st.write(f"(Step 2 of 6) Created the `{TEMP_TABLE_NAME}` temporary Snowflake table.")

        write_pandas(
            conn=snowflake_connection,
            df=st.session_state['recommended_songs_dataframe'],
            table_name=TEMP_TABLE_NAME,
            schema=SCHEMA_NAME,
            database=DATABASE_NAME,
        )
        st.write(f"(Step 3 of 6) Wrote pandas DataFrame data to `{TEMP_TABLE_NAME}`.")
        truncate_table_query: str = construct_truncate_table_query(table_name=TABLE_NAME)
        snowflake_cursor.execute(truncate_table_query)
        st.write(f"(Step 4 of 6) Removed old data from `{TABLE_NAME}`.")

        insert_data_query: str = construct_insert_data_query(table_name=TABLE_NAME, temp_table_name=TEMP_TABLE_NAME)
        snowflake_cursor.execute(insert_data_query)
        st.write(f"(Step 5 of 6) Inserted new data from `{TEMP_TABLE_NAME}` to`{TABLE_NAME}`.")

        drop_temp_table_query: str = construct_drop_table_query(table_name=TEMP_TABLE_NAME)
        snowflake_cursor.execute(drop_temp_table_query)
        st.write(f"(Step 6 of 6) Deleted `{TEMP_TABLE_NAME}`")

        # Commit the transaction
        snowflake_connection.commit()
        st.title("✅ Successfully saved recommended songs to Snowflake! ❄️")

        # Close the cursor and connection
        snowflake_cursor.close()
        snowflake_connection.close()

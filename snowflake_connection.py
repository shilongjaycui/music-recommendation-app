import os
import snowflake.connector

# Replace these variables with your actual Snowflake account details
USER = os.environ["SNOWFLAKE_USERNAME"]
PASSWORD = os.environ["SNOWFLAKE_PASSWORD"]
ACCOUNT = os.environ["SNOWFLAKE_ACCOUNT"]
WAREHOUSE = 'recommended_songs_warehouse'
DATABASE = 'recommended_songs_database'
SCHEMA = 'recommended_songs_schema'

if __name__ == "__main__":
    # Establish a connection
    conn = snowflake.connector.connect(
        user=USER,
        password=PASSWORD,
        account=ACCOUNT,
        warehouse=WAREHOUSE,
        database=DATABASE,
        schema=SCHEMA
    )

    # Create a cursor object
    cur = conn.cursor()

    # Create a database
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")

    # Create a schema
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")

    # Use the database and schema
    cur.execute(f"USE DATABASE {DATABASE}")
    cur.execute(f"USE SCHEMA {SCHEMA}")

    # Create a table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS my_table (
            id INT AUTOINCREMENT PRIMARY KEY,
            name STRING,
            age INT
        )
    """)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

install:
	pip install --upgrade pip
	pip install snowflake-connector-python

connect:
	python snowflake_connection.py
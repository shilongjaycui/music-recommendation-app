install:
	pip install --upgrade pip
	pip install pandas
	pip install snowflake-connector-python[pandas]
	pip install spotipy --upgrade

connect:
	python snowflake_connection.py

recommend:
	python get_recommended_songs.py
install:
	pip install --upgrade pip
	pip install snowflake-connector-python
	pip install spotipy --upgrade

connect:
	python snowflake_connection.py

recommend:
	python get_recommended_songs.py
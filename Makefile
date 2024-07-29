install:
	pip install --upgrade pip
	pip install pandas
	pip install snowflake-connector-python[pandas]
	pip install spotipy --upgrade
	pip install streamlit

run:
	streamlit run src/streamlit_app.py
# `snowflake-demo-app`
Based on your 5 favorite artists, here are the 20 songs that you're likely to also enjoy!

## Why (purpose)
To show off [Snowflake Connector for Python](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector) and [Spotipy](https://github.com/spotipy-dev/spotipy) (a lightweight Python library for the [Spotify Web API](https://developer.spotify.com/documentation/web-api))

## What (requirements)
- **Data Warehouse:** Structured data of the recommended songs based on your seed artists
- **Data Integration** Snowflake x Spotify Web API
- **AI / ML:** Now, how are those recommended songs similar to and different from one another? And in what ways?

## How (implementation)
- [x] version control: Git, GitHub
- [x] API: Python, Snowflake Connector for Python, Spotipy
- [x] UI: Streamlit
- [ ] AI/ML: [DataRobot](https://www.datarobot.com/)

## Running the web app locally

1. Clone this repo on your local machine:
   ```
   $ git clone git@github.com:shilongjaycui/snowflake-demo-app.git
   ```
2. Navigate into the data app:
   ```
   $ cd snowflake-demo-app
   ```
3. Create a Python virtual environment:
   ```
   $ python -m venv venv
   ```
4. Activate the virtual environment:
   ```
   $ source venv/bin/activate
   ```
5. Install dependencies:
   ```
   $ make install
   ```
6. Create a [Snowflake account](https://signup.snowflake.com/) and save your username, account, password as environment variables on your local machine. To verify the credentials are properly configured on your local machine, run the following command:
   ```
   $ env | grep SNOWFLAKE
   ```
   and you should see the following environment variables show up:
   ```
   SNOWFLAKE_USERNAME=<your-snowflake-username>
   SNOWFLAKE_ACCOUNT=<your-snowflake-account-id>
   SNOWFLAKE_PASSWORD=<your-snowflake-password>
   ```
7. Create an app in [Spotify for Developers](https://developer.spotify.com/dashboard) and save your app's client ID and client secret as environment variables on your local machine. To verify the credentials are properly configured on your local machine, run the following command:
   ```
   $ env | grep SPOTIPY
   ```
   and you should see the following environment variables show up:
   ```
   SPOTIPY_CLIENT_ID=<your-spotify-client-id>
   SPOTIPY_CLIENT_SECRET=<your-spotify-client-secret>
   ```
8. Run the Streamlit app:
   ```
   $ make run
   ```
# `snowflake-demo-app`
With Snowflake's help, I now know the most popular 10,000 songs on Spotify every morning when I wake up!

## Why (purpose)
To always know which 10,000 songs are the most popular on Spotify and how they're related to one another 🔎 🤨

## What (requirements)
- **Data Warehouse:** Structured data of the 10,000 most popular songs on Spotify
- **Data Integration** Data fetching mechanism that talks to the Spotify Web API every day
- **Data Analytics:** A playground for us to run SQL queries and answer questions about those 10,000 songs
- **AI / ML:** Now, how are those 10,000 songs similar to and different from one another? And in what ways?
  - maybe: integrate with [DataRobot](https://www.datarobot.com/)

## How (implementation)
- [x] version control: Git, GitHub
- [ ] backend: Python, [Spotipy](https://github.com/spotipy-dev/spotipy)
- [ ] frontend: TBD
- [ ] CI/CD: GitHub Actions
  - [ ] linting: flake8
  - [ ] testing: pytest

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

import sys
import os
import streamlit as st
from typing import List

# Make the `/api` folder importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.spotify_helper_functions import (  # pylint: disable=C0413
    Artist,
    Song,
    SEED_ARTISTS,
    SEED_TRACKS,
    SPOTIFY_API_CLIENT,
    get_several_artists,
    get_several_tracks,
)


def display_artist(artist: Artist):
    st.image(artist.image_url, use_column_width=True)
    st.markdown(f"### {artist.name}")
    st.markdown(", ".join(artist.genres))


def display_song(song: Song):
    st.image(song.album_image_url, use_column_width=True)
    st.markdown(f"### {song.name}")
    st.markdown(", ".join(song.artist_names))


def get_recommendation_button_styling(seed_name: str) -> str:
    styling: str = f"""
        <style>
        .centered-button {{
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }}
        .custom-button {{
            background-color: red; /* Red background */
            color: white; /* White text */
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold; /* Bold text */
            cursor: pointer;
            text-align: center;
        }}
        .custom-button:hover {{
            background-color: darkred; /* Darker red on hover */
        }}
        </style>
        <div class="centered-button">
            <button class="custom-button" onclick="window.location.href='#';">Recommend songs based on the {seed_name}s</button>
        </div>
    """
    return styling


st.title("Artists")
artists: List[Artist] = get_several_artists(
    api_client=SPOTIFY_API_CLIENT,
    spotify_urls=list(SEED_ARTISTS.values()),
)
# Create columns
cols = st.columns(len(artists))
# Display each artist in a column
for col, artist in zip(cols, artists):
    with col:
        display_artist(artist)
# Add a styled button below the artist display
st.markdown(get_recommendation_button_styling(seed_name="artist"), unsafe_allow_html=True)


st.title("Songs")
songs: List[Song] = get_several_tracks(
    api_client=SPOTIFY_API_CLIENT,
    spotify_urls=list(SEED_TRACKS.values()),
)
# Create columns
cols = st.columns(len(songs))
# Display each artist in a column
for col, song in zip(cols, songs):
    with col:
        display_song(song)
# Add a styled button below the artist display
st.markdown(get_recommendation_button_styling(seed_name="song"), unsafe_allow_html=True)

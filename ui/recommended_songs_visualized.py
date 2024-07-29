import sys
import os
import streamlit as st
import pandas as pd
from typing import List, Dict

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
    get_recommended_songs_based_on_artists,
    get_recommended_songs_based_on_other_songs,
    construct_recommended_songs_dataframe,
)


def display_artist(artist: Artist):
    st.image(artist.artist_image_url, use_column_width=True)
    st.markdown(f"### {artist.artist_name}")
    st.markdown(", ".join(artist.artist_genres))


def display_song(song: Song):
    st.image(song.album_image_url, use_column_width=True)
    st.markdown(f"### {song.song_name}")
    st.markdown(", ".join(song.artist_names))


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

if st.button('Get recommended songs based on the artists'):
    recommended_songs: List[Dict] = get_recommended_songs_based_on_artists(
        api_client=SPOTIFY_API_CLIENT,
        seed_artists=list(SEED_ARTISTS.values()),
        recommendation_size=10,
    )
    recommended_songs_dataframe: pd.DataFrame = construct_recommended_songs_dataframe(recommended_songs=recommended_songs)

    # Display the DataFrame
    st.dataframe(recommended_songs_dataframe)

# Songs Section
st.title("Songs")
songs: List[Song] = get_several_tracks(
    api_client=SPOTIFY_API_CLIENT,
    spotify_urls=list(SEED_TRACKS.values()),
)
# Create columns for songs
cols = st.columns([1 for _ in songs])
# Display each song in a column
for col, song in zip(cols, songs):
    with col:
        display_song(song)

if st.button('Get recommended songs based on the songs'):
    recommended_songs: List[Dict] = get_recommended_songs_based_on_other_songs(
        api_client=SPOTIFY_API_CLIENT,
        seed_tracks=list(SEED_TRACKS.values()),
        recommendation_size=10,
    )
    recommended_songs_dataframe: pd.DataFrame = construct_recommended_songs_dataframe(recommended_songs=recommended_songs)

    # Display the DataFrame
    st.dataframe(recommended_songs_dataframe)
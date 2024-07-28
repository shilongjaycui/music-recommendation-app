import os
from typing import List, Dict
from dataclasses import dataclass
import pandas as pd

import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


@dataclass
class Song:
    song_name: str
    song_url: str
    song_popularity: int
    artist_names: List[str]
    artist_urls: List[str]


SEED_ARTISTS: Dict[str, str] = {
    "Maluma": "https://open.spotify.com/artist/1r4hJ1h58CWwUQe3MxPuau",
    "Anitta": "https://open.spotify.com/artist/7FNnA9vBm6EKceENgCGRMb",
    "J Balvin": "https://open.spotify.com/artist/1vyhD5VmyZ7KMfW5gqLgo5",
    "Daddy Yankee": "https://open.spotify.com/artist/4VMYDCV2IEDYJArk749S6m",
    "Angelina Mango": "https://open.spotify.com/artist/1A6HBLulvBFzNtlMb7b08f",
}

SEED_GENRES: List[str] = []

SEED_TRACKS: Dict[str, str] = {
    "Hawái": "https://open.spotify.com/track/1yoMvmasuxZfqHEipJhRbp",
    "BELLAKEO": "https://open.spotify.com/track/5Fohh8kl8403DSoq4KH7Ll",
    "X": "https://open.spotify.com/track/5YUyW9opqNsMSEzzecZih1",
    "Con Calma": "https://open.spotify.com/track/5w9c2J52mkdntKOmRLeM2m",
    "che t'o dico a fa'": "https://open.spotify.com/track/29BLybpYHhOcDGWfkvKNTu",
}

CLIENT_CREDENTIALS_FLOW_MANAGER = SpotifyClientCredentials(
    client_id=os.environ["SPOTIPY_CLIENT_ID"],
    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
)
SPOTIFY_API_CLIENT = spotipy.Spotify(auth_manager=CLIENT_CREDENTIALS_FLOW_MANAGER)


def get_recommended_songs_based_on_artists(
    api_client: Spotify,
    seed_artists: List[str],
    recommendation_size: int,
) -> List[Dict]:
    songs: List[Dict] = api_client.recommendations(
        seed_artists=seed_artists,
        limit=recommendation_size,
    )["tracks"]

    return songs


def get_recommended_songs_based_on_other_songs(
    api_client: Spotify,
    seed_tracks: List[str],
    recommendation_size: int,
) -> List[Dict]:
    songs: List[Dict] = api_client.recommendations(
        seed_tracks=seed_tracks,
        limit=recommendation_size,
    )["tracks"]

    return songs


def get_recommended_songs_based_on_genres(
    api_client: Spotify,
    seed_genres: List[str],
    recommendation_size: int,
) -> List[Dict]:
    songs: List[Dict] = api_client.recommendations(
        seed_genres=seed_genres,
        limit=recommendation_size,
    )["tracks"]

    return songs


def construct_recommended_songs_dataframe(recommended_songs: List[Dict]):
    songs: List[Song] = []
    for recommended_song in recommended_songs:
        songs.append(Song(
            song_name=recommended_song["name"],
            song_url=recommended_song["external_urls"]["spotify"],
            song_popularity=recommended_song["popularity"],
            artist_names=[artist["name"] for artist in recommended_song["artists"]],
            artist_urls=[artist["external_urls"]["spotify"] for artist in recommended_song["artists"]],
        ))

    df = pd.DataFrame([song.__dict__ for song in songs])
    df.columns = map(lambda x: str(x).upper(), df.columns)  # The pandas DataFrame columns must be all uppercase in order to avoid the `invalid identifier` SQL compilation error
    print(f"recommended songs dataframe columns: {df.columns}")
    return df

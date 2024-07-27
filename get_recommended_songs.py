import os
from typing import Dict, List
import pandas as pd

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


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


if __name__ == "__main__":
    recommended_songs: List[Dict] = SPOTIFY_API_CLIENT.recommendations(
        seed_artists=list(SEED_ARTISTS.values()),
        limit=100,
    )["tracks"]
    recommended_songs_dict: Dict[str, List] = {
        "song name": [],
        "song URL": [],
        "song popularity": [],
        "artist names": [],
        "artist URLs": [],
    }
    for recommended_song in recommended_songs:
        print(f"recommended song: {recommended_song}")
        recommended_songs_dict["song name"].append(recommended_song["name"])
        recommended_songs_dict["song URL"].append(recommended_song["external_urls"]["spotify"])
        recommended_songs_dict["song popularity"].append(recommended_song["popularity"])
        recommended_songs_dict["artist names"].append([artist["name"] for artist in recommended_song["artists"]])
        recommended_songs_dict["artist URLs"].append([artist["external_urls"]["spotify"] for artist in recommended_song["artists"]])
    recommended_songs_df = pd.DataFrame.from_dict(recommended_songs_dict)

    print(f"Recommended songs df:\n{recommended_songs_df}")

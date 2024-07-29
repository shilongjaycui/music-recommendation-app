import os
from typing import List, Dict
from dataclasses import dataclass
import pandas as pd

import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


@dataclass
class Artist:
    artist_name: str
    artist_genres: List[str]
    artist_image_url: str


@dataclass
class Song:
    song_name: str
    song_url: str
    song_popularity: int
    artist_names: List[str]
    artist_urls: List[str]
    album_image_url: str


SEED_ARTISTS: Dict[str, str] = {
    "Maluma": "https://open.spotify.com/artist/1r4hJ1h58CWwUQe3MxPuau",
    "Anitta": "https://open.spotify.com/artist/7FNnA9vBm6EKceENgCGRMb",
    "J Balvin": "https://open.spotify.com/artist/1vyhD5VmyZ7KMfW5gqLgo5",
    "Daddy Yankee": "https://open.spotify.com/artist/4VMYDCV2IEDYJArk749S6m",
    "Shakira": "https://open.spotify.com/artist/0EmeFodog0BfCgMzAIvKQp",
}

SEED_TRACKS: Dict[str, str] = {
    "Hawái": "https://open.spotify.com/track/1yoMvmasuxZfqHEipJhRbp",
    "BELLAKEO": "https://open.spotify.com/track/5Fohh8kl8403DSoq4KH7Ll",
    "X": "https://open.spotify.com/track/5YUyW9opqNsMSEzzecZih1",
    "Con Calma": "https://open.spotify.com/track/5w9c2J52mkdntKOmRLeM2m",
    "TQG": "https://open.spotify.com/track/0DWdj2oZMBFSzRsi2Cvfzf",
}

CLIENT_CREDENTIALS_FLOW_MANAGER = SpotifyClientCredentials(
    client_id=os.environ["SPOTIPY_CLIENT_ID"],
    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
)
SPOTIFY_API_CLIENT = spotipy.Spotify(auth_manager=CLIENT_CREDENTIALS_FLOW_MANAGER)


def get_several_artists(api_client: Spotify, spotify_urls: List[str]) -> List[Artist]:
    response: Dict = api_client.artists(artists=spotify_urls)
    artist_list: List[Dict] = response["artists"]
    artists = []
    for artist_json in artist_list:
        artist = Artist(
            artist_name=artist_json["name"],
            artist_genres=artist_json["genres"],
            artist_image_url=artist_json["images"][0]["url"],
        )
        artists.append(artist)
    return artists


def get_several_tracks(api_client: Spotify, spotify_urls: List[str]) -> List[Song]:
    response: Dict = api_client.tracks(tracks=spotify_urls)
    track_list: List[Dict] = response["tracks"]
    tracks: List[Song] = []
    for track_json in track_list:
        track = Song(
            song_name=track_json["name"],
            song_url=track_json["external_urls"]["spotify"],
            song_popularity=track_json["popularity"],
            artist_names=[artist["name"] for artist in track_json["artists"]],
            artist_urls=[artist["external_urls"]["spotify"] for artist in track_json["artists"]],
            album_image_url=track_json["album"]["images"][0]["url"],
        )
        tracks.append(track)
    return tracks


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


def construct_recommended_songs_dataframe(recommended_songs: List[Dict]):
    recommended_songs_urls: List[str] = [recommended_song["external_urls"]["spotify"] for recommended_song in recommended_songs]
    songs: List[Song] = get_several_tracks(api_client=SPOTIFY_API_CLIENT, spotify_urls=recommended_songs_urls)

    df = pd.DataFrame([song.__dict__ for song in songs])
    df.columns = map(lambda x: str(x).upper(), df.columns)  # The pandas DataFrame columns must be all uppercase in order to avoid the `invalid identifier` SQL compilation error
    print(f"recommended songs dataframe columns: {df.columns}")
    return df

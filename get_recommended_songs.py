import os
from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


SEED_ARTISTS: Dict[str, str] = {
    "Maluma": "1r4hJ1h58CWwUQe3MxPuau",
    "Anitta": "7FNnA9vBm6EKceENgCGRMb",
    "J Balvin": "1vyhD5VmyZ7KMfW5gqLgo5",
    "Daddy Yankee": "4VMYDCV2IEDYJArk749S6m",
    "Angelina Mango": "1A6HBLulvBFzNtlMb7b08f",
}

SEED_GENRES: List[str] = []

SEED_TRACKS: Dict[str, str] = {
    "Hawái": "1yoMvmasuxZfqHEipJhRbp",
    "BELLAKEO": "5Fohh8kl8403DSoq4KH7Ll",
    "X": "5YUyW9opqNsMSEzzecZih1",
    "Con Calma": "5w9c2J52mkdntKOmRLeM2m",
    "che t'o dico a fa'": "29BLybpYHhOcDGWfkvKNTu",
}

auth_manager = SpotifyClientCredentials(
    client_id=os.environ["SPOTIPY_CLIENT_ID"],
    client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
)
sp = spotipy.Spotify(auth_manager=auth_manager)


if __name__ == "__main__":
    playlists = sp.user_playlists('spotify')
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

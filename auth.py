import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

ENVIRON_KEY_CLIENT_ID = 'SPOTIFY_CLIENT_ID'
ENVIRON_KEY_CLIENT_SECRET = 'SPOTIFY_CLIENT_SECRET'


def new_client() -> spotipy.Spotify:
    client_id = os.environ.get(ENVIRON_KEY_CLIENT_ID)
    if not client_id:
        raise ValueError(f'No value for ${ENVIRON_KEY_CLIENT_ID} found in environ')
    client_secret = os.environ.get(ENVIRON_KEY_CLIENT_SECRET)
    if not client_secret:
        raise ValueError(f'No value for ${ENVIRON_KEY_CLIENT_SECRET} found in environ')

    return spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret,
    ))

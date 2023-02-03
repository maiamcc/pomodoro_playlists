import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

ENVIRON_KEY_CLIENT_ID = 'SPOTIFY_CLIENT_ID'
ENVIRON_KEY_CLIENT_SECRET = 'SPOTIFY_CLIENT_SECRET'

# probably don't need all of these idk
SCOPES = ['playlist-read-private',
          'playlist-read-collaborative',
          'playlist-modify-private',
          'playlist-modify-public',
          'user-read-email',
          'user-read-private']


def new_client() -> spotipy.Spotify:
    client_id = os.environ.get(ENVIRON_KEY_CLIENT_ID)
    if not client_id:
        raise ValueError(f'No value for ${ENVIRON_KEY_CLIENT_ID} found in environ')
    client_secret = os.environ.get(ENVIRON_KEY_CLIENT_SECRET)
    if not client_secret:
        raise ValueError(f'No value for ${ENVIRON_KEY_CLIENT_SECRET} found in environ')

    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        scope=' '.join(SCOPES),
        redirect_uri='http://127.0.0.1:8080',
    ))

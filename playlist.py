from datetime import datetime
import typing as t

import spotipy

import track

# there should be a way to get the current user from the client but it's throwing 401 Unauthorized
# and I don't know why, so hardcode me for now.


USER = 'maianess'


class Playlist:
    def __init__(self, name: str, id: str, uri: str):
        self.name = name
        self.url = f'https://open.spotify.com/playlist/{id}'
        self.uri = uri

    @classmethod
    def from_dict(cls, d: dict) -> 'Playlist':
        name = d['name']
        id = d['id']
        uri = d['uri']

        return Playlist(name, id, uri)

    def add_tracks(self, cli: spotipy.Spotify, tracks: t.List[track.Uri]):
        cli.playlist_add_items(self.uri, tracks)


def new_playlist(cli: spotipy.Spotify, playlist_name: t.Optional[str] = None) -> Playlist:
    # TODO: description maybe?
    if playlist_name is None:
        playlist_name = f'Awesome Playlist {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'
    resp = cli.user_playlist_create(USER, playlist_name)
    return Playlist.from_dict(resp)

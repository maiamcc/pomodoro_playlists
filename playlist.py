from datetime import datetime
from typing import List, Optional

import spotipy

import track
import user


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

    def add_tracks(self, cli: spotipy.Spotify, tracks: List[track.Uri]):
        cli.playlist_add_items(self.uri, tracks)


def new_playlist(cli: spotipy.Spotify, playlist_name: Optional[str] = None) -> Playlist:
    # TODO: description maybe?
    if playlist_name is None:
        playlist_name = f'Awesome Playlist {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}'
    resp = cli.user_playlist_create(user.current_user(cli), playlist_name)
    return Playlist.from_dict(resp)


def assemble_playlist(cli: spotipy.Spotify, max_cycles: int, rounds_per_cycle: int, breaks_between_cycles: int,
                      work_buckets: List[List[track.Track]], break_buckets: List[List[track.Track]],
                      playlist_name: Optional[str] = None) -> Playlist:

    playlist = new_playlist(cli, playlist_name=playlist_name)

    for _ in range(max_cycles):
        for i in range(rounds_per_cycle):
            if work_buckets and break_buckets:  # if we still have tracks available
                playlist.add_tracks(cli, [t.uri for t in work_buckets.pop()])
                playlist.add_tracks(cli, [t.uri for t in break_buckets.pop()])
            else:
                print('not enough groups of stuff to keep going, sorry :-/')
                return playlist

        for i in range(breaks_between_cycles - 1):  # nb: already added one break at the end of the previous loop
            if break_buckets:
                playlist.add_tracks(cli, [t.uri for t in break_buckets.pop()])
            else:
                print('not enough groups of stuff to keep going, sorry :-/')
                return playlist

    return playlist

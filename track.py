from typing import List

import binpacking
import spotipy

Uri = str


class Track:
    def __init__(self, duration_ms: int, uri: Uri):
        self.duration_secs = duration_ms / 1000  # todo: store as time.duration
        self.uri = uri

    @classmethod
    def from_dict(cls, d: dict) -> 'Track':
        duration_ms = d['duration_ms']
        uri = d['uri']

        return Track(duration_ms, uri)


# TODO: subclass spotipy client?
def get_tracks(cli, url: str) -> List[Track]:
    if 'open.spotify.com/' not in url:
        raise ValueError(f'URL f{url} doesn\'t seem to be a valid Spotify url (should contain "open.spotify.com/"')

    if 'open.spotify.com/playlist' in url:
        return _tracks_from_playlist(cli, url)
    elif 'open.spotify.com/album' in url:
        return _tracks_from_album(cli, url)
    else:
        raise ValueError(f'Unrecognized Spotify URL. This program currently only supports playlists ("/playlist/...") and albums ("/album/...")')


def _tracks_from_album(cli: spotipy.Spotify, album_url: str) -> List[Track]:
    results = cli.album_tracks(album_url)
    tracks = results['items']
    while results['next']:
        results = cli.next(results)
        tracks.extend(results['items'])

    return [Track.from_dict(track) for track in tracks]


def _tracks_from_playlist(cli: spotipy.Spotify, playlist_url: str) -> List[Track]:
    results = cli.playlist_items(playlist_url)
    tracks = [item['track'] for item in results['items']]
    while results['next']:
        results = cli.next(results)
        tracks.extend([item['track'] for item in results['items']])

    return [Track.from_dict(track) for track in tracks]


def _tracks_from_results(cli: spotipy.Spotify, results_dict: dict) -> List[Track]:
    tracks = results_dict['items']
    while results_dict['next']:
        results_dict = cli.next(results_dict)
        tracks.extend(results_dict['items'])

    return [Track.from_dict(track) for track in tracks]


# TODO: pass margin? is there a way to target a certain bucket value with a margin over?
def bucket_tracks_by_duration(tracks: List[Track], duration_secs: int) -> List[List[Track]]:
    return binpacking.to_constant_volume(tracks, duration_secs, key=lambda t: t.duration_secs)



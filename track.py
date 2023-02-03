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
        duration_ms = d.get('duration_ms')
        uri = d.get('uri')

        return Track(duration_ms, uri)


# TODO: subclass spotipy client?
def get_tracks(cli, identifier: str) -> List[Track]:
    # TODO: this currently only supports albums—
    #   get tracks from playlists as well, maybe artists?
    return _tracks_from_album(cli, identifier)


def _tracks_from_album(cli: spotipy.Spotify, album_identifier: str) -> List[Track]:
    # NB: `album_identifier` may be the album ID, URI or URL
    results = cli.album_tracks(album_identifier)
    tracks = results['items']
    while results['next']:
        results = cli.next(results)
        tracks.extend(results['items'])

    return [Track.from_dict(track) for track in tracks]


# TODO: pass margin? is there a way to target a certain bucket value with a margin over?
def bucket_tracks_by_duration(tracks: Track, duration_secs: int) -> List[List[Track]]:
    return binpacking.to_constant_volume(tracks, duration_secs, key=lambda t: t.duration_secs)



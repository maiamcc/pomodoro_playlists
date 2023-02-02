import typing as t

import spotipy


class Track:
    def __init__(self, duration_ms: int, uri: str):
        self.duration_ms = duration_ms  # todo: store as time.duration
        self.uri = uri

    @classmethod
    def from_dict(cls, d: dict) -> 'Track':
        duration_ms = d.get('duration_ms')
        uri = d.get('uri')

        return Track(duration_ms, uri)


# TODO: subclass spotipy client?
# TODO: get tracks from playlists as well, maybe artists?
def tracks_from_album(cli: spotipy.Spotify, album_identifier: str) -> t.List[Track]:
    # NB: `album_identifier` may be the album ID, URI or URL
    results = cli.album_tracks(album_identifier)
    tracks = results['items']
    while results['next']:
        results = cli.next(results)
        tracks.extend(results['items'])

    return [Track.from_dict(track) for track in tracks]


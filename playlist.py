import typing as t

import spotipy


# there should be a way to get the current user from the client but it's throwing 401 Unauthorized
# and I don't know why, so hardcode me for now.

USER = 'maianess'
def new_playlist(cli: spotipy.Spotify, playlist_name: str) -> t.List[Track]:
    cli.user_playlists()
    # user_playlist_create(user, name, public=True, collaborative=False, description='')
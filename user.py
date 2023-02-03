# A singleton, so we don't need to fetch this information more than once per run.
import spotipy

_CURRENT_USER = None


def current_user(cli: spotipy.Spotify) -> str:
    """Get the current user (if one is authenticated; otherwise, authenticate and get the current user).

    NB: I have no idea how this authentication will work for anyone besides me, wheeeee.
    """
    global _CURRENT_USER
    if not _CURRENT_USER:
        me_response = cli.me()
        _CURRENT_USER = me_response['id']
    return _CURRENT_USER

#! /usr/bin/env python

from auth import new_client

from playlist import new_playlist
from track import get_tracks

POMO_ROUNDS = 4
# Anticipated args:
#   - work music (album or playlist identifier)
#   - break music (album or playlist identifier)
#   - optional: target playlist id (otherwise, create a new one)
#   - optional: preserve order = t/f (if true, we try to create a pomo
#       playlist by keeping tracks in order from 'work' and 'break' music;
#       otherwise we just grab tracks of appropriate length from wherever
#   - optional: work interval; break interval; num cycles before long break; etc.


def main():
    # album url: bach preludes and fugues
    work_music_identifier = 'https://open.spotify.com/album/66zilH1HJzRLEorco0u6bS?si=SJ4fATSBSN6LbhDkLQ2tbw'

    # album url: "chill techno transformation"
    break_music_identifier = 'https://open.spotify.com/album/29Tt0fcqRrfsW1OCGB7lNH?si=V8bmcM6CQE2DP0_cUCdjsA'

    cli = new_client()

    work_tracks = get_tracks(cli, work_music_identifier)
    break_tracks = get_tracks(cli, break_music_identifier)

    # TODO: authenticate, somehow

    playlist = new_playlist(cli)
    work_i = 0
    break_i = 0
    for rnd in range(POMO_ROUNDS):
        playlist.add_tracks(cli, [t.uri for t in work_tracks[work_i:work_i+5]])
        work_i += 6
        playlist.add_tracks(cli, [t.uri for t in break_tracks[break_i:break_i+2]])
        break_i += 3

    print(f'made u a nice playlist, champ! {playlist.url}')


if __name__ == '__main__':
    main()


#! /usr/bin/env python

from auth import new_client

from playlist import new_playlist
from track import get_tracks, bucket_tracks_by_duration

POMO_ROUNDS = 4
WORK_DUR_MINS = 25
BREAK_DUR_MINS = 5

WORK_DUR_SECS = WORK_DUR_MINS * 60
BREAK_DUR_SECS = BREAK_DUR_MINS * 60

# Anticipated args:
#   - work music (album or playlist identifier)
#   - break music (album or playlist identifier)
#   - optional: target playlist id (otherwise, create a new one)
#   - optional: preserve order = t/f (if true, we try to create a pomo
#       playlist by keeping tracks in order from 'work' and 'break' music;
#       otherwise we just grab tracks of appropriate length from wherever
#   - optional: work interval; break interval; num cycles before long break; etc.


def main():
    work_music_identifier = 'https://open.spotify.com/playlist/2MyJEE4F1Xo4nw4WBnfwiP'
    break_music_identifier = 'https://open.spotify.com/album/29Tt0fcqRrfsW1OCGB7lNH?si=V8bmcM6CQE2DP0_cUCdjsA'

    cli = new_client()

    work_tracks = get_tracks(cli, work_music_identifier)
    break_tracks = get_tracks(cli, break_music_identifier)

    work_buckets = bucket_tracks_by_duration(work_tracks, WORK_DUR_SECS)
    break_buckets = bucket_tracks_by_duration(break_tracks, BREAK_DUR_SECS)

    # TODO: authenticate, somehow

    playlist = new_playlist(cli)
    for i in range(POMO_ROUNDS):
        if i < len(work_buckets) and i < len(break_buckets):
            playlist.add_tracks(cli, [t.uri for t in work_buckets[i]])
            playlist.add_tracks(cli, [t.uri for t in break_buckets[i]])
        else:
            print('not enough groups of stuff to keep going, sorry :-/')

    print(f'made u a nice playlist, champ! {playlist.url}')


if __name__ == '__main__':
    main()


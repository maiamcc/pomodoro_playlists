#! /usr/bin/env python
import math

from auth import new_client
from playlist import new_playlist
from track import get_tracks, bucket_tracks_by_duration

POMO_ROUNDS = 4
WORK_DUR_MINS = 25
WORK_FLEX_MINS = 5   # amt by which we're willing to go over work duration
BREAK_DUR_MINS = 6
BREAK_FLEX_MINS = 2.5  # amt by which we're willing to go over break duration

WORK_DUR_SECS = math.floor((WORK_DUR_MINS + WORK_FLEX_MINS) * 60)
BREAK_DUR_SECS = math.floor((BREAK_DUR_MINS + BREAK_FLEX_MINS) * 60)

# Anticipated args:
#   - work music (album or playlist identifier)
#   - break music (album or playlist identifier)
#   - optional: playlist name
#   - optional: work interval; break interval; num cycles before long break; etc.
#   - optional: target playlist id (otherwise, create a new one)
#   - optional: preserve order = t/f (if true, we try to create a pomo
#       playlist by keeping tracks in order from 'work' and 'break' music;
#       otherwise we just grab tracks of appropriate length from wherever


def main():
    work_music_identifier = 'https://open.spotify.com/playlist/2MyJEE4F1Xo4nw4WBnfwiP'
    break_music_identifier = 'https://open.spotify.com/album/29Tt0fcqRrfsW1OCGB7lNH?si=V8bmcM6CQE2DP0_cUCdjsA'

    cli = new_client()

    work_tracks = get_tracks(cli, work_music_identifier)
    break_tracks = get_tracks(cli, break_music_identifier)

    work_buckets = bucket_tracks_by_duration(work_tracks, WORK_DUR_SECS)
    break_buckets = bucket_tracks_by_duration(break_tracks, BREAK_DUR_SECS)

    playlist = new_playlist(cli)

    for i in range(POMO_ROUNDS):
        if i < len(work_buckets) and i < len(break_buckets):
            playlist.add_tracks(cli, [t.uri for t in work_buckets[i]])
            playlist.add_tracks(cli, [t.uri for t in break_buckets[i]])
        else:
            print('not enough groups of stuff to keep going, sorry :-/')

    print(f'made u a nice playlist, champ! {playlist.url}')
    print('Happy 🍅!!')


if __name__ == '__main__':
    main()


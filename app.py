#! /usr/bin/env python

import argparse
import math

from auth import new_client
from playlist import assemble_playlist
from track import get_tracks, bucket_tracks_by_duration

DEFAULT_CYCLES = 5
DEFAULT_ROUNDS_PER_CYCLE = 4
DEFAULT_BREAKS_BETWEEN_CYCLES = 3
DEFAULT_WORK_DUR_MINS = 25
DEFAULT_BREAK_DUR_MINS = 5
WORK_FLEX_MINS = 5   # amt by which we're willing to go over work duration
BREAK_FLEX_MINS = 2  # amt by which we're willing to go over break duration

# Possible args for future:
#   - optional: target playlist id (otherwise, create a new one)
#   - optional: flex_mins configurable
#   - optional: preserve order = t/f (if true, we try to create a pomo
#       playlist by keeping tracks in order from 'work' and 'break' music;
#       otherwise we just grab tracks of appropriate length from wherever


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'work_music',
        type=str,
        help='url for album / playlist / artist to use as work music'
    )
    parser.add_argument(
        'break_music',
        type=str,
        help='url for album / playlist / artist to use as break music'
    )
    parser.add_argument(
        '--title', '-t',
        type=str,
        help='title for resulting playlist'
    )
    parser.add_argument(
        '--work_mins', '-w',
        type=int,
        default=DEFAULT_WORK_DUR_MINS,
        help='length of a work block, in minutes'
    )
    parser.add_argument(
        '--break_mins', '-b',
        type=int,
        default=DEFAULT_BREAK_DUR_MINS,
        help='length of a break block, in minutes'
    )
    # todo: should work/break flex be settable?
    parser.add_argument(
        '--rounds', '-r',
        type=int,
        default=DEFAULT_ROUNDS_PER_CYCLE,
        help='number of rounds in a cycle (i.e. number of rounds before a long break)'
    )
    parser.add_argument(
        '--cycles', '-c',
        type=int,
        default=DEFAULT_CYCLES,
        help='maximum number of cycles in a playlist (though playlist length is '
             'also constrained by amount of available material)'
    )
    parser.add_argument(
        '--breaks-between', '-bb',
        type=int,
        default=DEFAULT_BREAKS_BETWEEN_CYCLES,
        help='number of breaks between cycles (basically this determines the length of a long break)'
    )

    return parser


def main():
    parser = argument_parser()
    args = parser.parse_args()

    cli = new_client()

    work_tracks = get_tracks(cli, args.work_music)
    break_tracks = get_tracks(cli, args.break_music)

    work_buckets = bucket_tracks_by_duration(work_tracks, args.work_mins, WORK_FLEX_MINS)
    break_buckets = bucket_tracks_by_duration(break_tracks, args.break_mins, BREAK_FLEX_MINS)

    playlist = assemble_playlist(cli, args.cycles, args.rounds, args.breaks_between,
                                 work_buckets, break_buckets, args.title)

    print()
    print(f'made u a nice playlist, champ! {playlist.url}')
    print('Happy ????!!')


if __name__ == '__main__':
    main()


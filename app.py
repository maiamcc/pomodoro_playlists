#! /usr/bin/env python

from auth import new_client

from track import tracks_from_album

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

    tracks = tracks_from_album(cli, work_music_identifier)
    me = cli.me()

if __name__ == '__main__':
    main()


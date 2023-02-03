# Pomodoro Playlists

Given some music for working and some music for breaks, generate a pomodoro playlist: ~25m of work music followed by ~5m of break music.

1. optionally, create a virtualenv to store your stuff and activate it
2. `pip install -r requirements.txt`
3. [create a Spotify app](https://developer.spotify.com/dashboard/applications) (and in app settings, set "redirect URI" to `http://127.0.0.1:8080`)
4. put your app credentials in your environ
    ```
    export SPOTIFY_CLIENT_ID='xxx'
    export SPOTIFY_CLIENT_SECRET='yyy'
    ```
   * or if we're buds, just ask me to lend you my creds
5. generate your playlist with `./app.py [work_music_url] [break_music_url] [...settings...]` (see `./app.py -h` for full usage instructions).
    * the `work|break_music_url` parameters may be any `open.spotify.com` URL for a playlist, album, or artist. (To get this URL, find the music in question, and navigate to "..." > "share" > "copy link".)
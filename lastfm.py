import json
import argparse
import pylast
import datetime
import pytz

# Load the API keys from the config file
with open("config.json") as f:
    config = json.load(f)

API_KEY = config['lastfm_api_key']
API_SECRET = config['lastfm_api_secret']

# In order to perform a write operation you need to authenticate yourself
username = "arnavsurve"
password_hash = pylast.md5(config['password'])

lastfm_network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)


def get_top_tracks(username, number):
    top_tracks = lastfm_network.get_user(username).get_top_tracks(period='7day', limit=number)
    formatted_tracks = []

    for track in top_tracks:
        formatted_tracks.append({
            'title': track.item.title,
            'artist': track.item.artist.name,
            'play-count': track.weight
        })
    return formatted_tracks


def get_recent_tracks(username, number):
    recent_tracks = lastfm_network.get_user(username).get_recent_tracks(limit=number)
    formatted_tracks = []

    for track in recent_tracks:
        track_info = track_and_timestamp(track)
        formatted_tracks.append({
            'playback_date': track.playback_date,
            'artist': track.track.artist.name,
            'track': track.track.title,
            'time_str': track_info['time_str']
        })
    print(formatted_tracks)
    return formatted_tracks


def track_and_timestamp(track):
    playback_datetime = datetime.datetime.strptime(track.playback_date, "%d %b %Y, %H:%M")
    playback_datetime = playback_datetime.replace(tzinfo=pytz.UTC)

    # get current time in UTC
    now_utc = datetime.datetime.now(pytz.UTC)

    # calculate time difference
    time_difference = now_utc - playback_datetime

    # convert time difference to readable format
    days, remainder = divmod(time_difference.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # format and return track information with time elapsed
    if days > 0:
        time_str = f"{int(days)} days, {int(hours)} hours ago"
    elif hours > 0 and hours < 2:
        time_str = f"{int(hours)} hour, {int(minutes)} minutes ago"
    elif hours > 1:
        time_str = f"{int(hours)} hours, {int(minutes)} minutes ago"
    else:
        time_str = f"{int(minutes)} minutes ago"

    return {
        'playback_date': playback_datetime,
        'time_str': time_str,
        'track': track.track.title,
        'artist': track.track.artist.name
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-u", "--username", help="Last.fm username")
    parser.add_argument(
        "-n",
        "--number",
        default=20,
        type=int,
        help="Number of tracks to show (when no artist given)",
    )
    args = parser.parse_args()

    if not args.username:
        args.username = username

    print(args.username + " last played:")
    try:
        get_recent_tracks(args.username, args.number)
    except pylast.WSError as e:
        print("Error: " + str(e))

    print("\n" + args.username + " top tracks:")
    try:
        get_top_tracks(args.username, args.number)
    except pylast.WSError as e:
        print("Error: " + str(e))

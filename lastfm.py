import json
import argparse
import pylast

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

    for i, track in enumerate(top_tracks):
        print(f"{i+1} {track.item.title} by {track.item.artist.name} - {track.weight} scrobbles")
    return top_tracks


def get_recent_tracks(username, number):
    recent_tracks = lastfm_network.get_user(username).get_recent_tracks(limit=number)

    for i, track in enumerate(recent_tracks):
        printable = track_and_timestamp(track)
        print(str(i + 1) + " " + printable)
    return recent_tracks


def track_and_timestamp(track):
    return f"{track.playback_date}\t{track.track}"


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

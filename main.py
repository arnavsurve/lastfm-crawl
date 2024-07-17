from flask import Flask, request, jsonify
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
from lastfm import get_recent_tracks, get_top_tracks

app = Flask(__name__)

# # initialize rate limiter
# limiter = Limiter(
#     app,
#     key_func=get_remote_address,
#     default_limits=["100 per day", "10 per hour"]
# )

@app.route("/", methods=["GET"])
def home():
    return "server is running!"

@app.route("/recent-tracks", methods=["GET"])
def recent_tracks():
    username = request.args.get("username", type=str)
    number = request.args.get("number", default=20, type=int)

    try:
        tracks = get_recent_tracks(username, number)
        # convert tracks to JSON compatible format
        tracks_list = [{'payback_date': track.playback_date, 'track': str(track.track)} for track in tracks]
        return jsonify(tracks_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/top-tracks", methods=["GET"])
def top_tracks():
    username = request.args.get("username", type=str)
    number = request.args.get("number", default=10, type=int)

    try:
        tracks = get_top_tracks(username, number)
        if tracks is None:
            tracks = []
        # convert tracks to JSON compatible format
        tracks_list = [{'title': track.item.title, 'artist': track.item.artist.name, 'play-count':track.weight} for track in tracks]
        return jsonify(tracks_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()

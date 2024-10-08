from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
from psnawp_api import PSNAWP

from database import insert_playing_time_into_db, get_playing_time_from_db
from psn_functions import (
    get_personal_info,
    get_registered_devices,
    get_user_info,
    search_game_titles, trophy_titles
)

app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests by default for all routes

# Global variables to store user account info, PSNAWP instance, and authentication data
cached_client = None
psnawp = None
auth_data = {
    "npsso_code": None,
    "expiration": None
}

# Function to check if the npsso_code is still valid
def is_npsso_code_valid():
    if auth_data['npsso_code'] and auth_data['expiration']:
        return datetime.now() < auth_data['expiration']
    return False

# Route to authenticate and store the NPSSO code with expiration
@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    global cached_client, psnawp, auth_data
    npsso_code = request.json.get('npsso_code')

    if not npsso_code:
        return jsonify({"error": "NPSSO code is required."}), 400

    # Initialize PSNAWP with the provided NPSSO code
    psnawp = PSNAWP(npsso_code)
    cached_client = psnawp.me()  # Call psnawp.me() once and store the result

    # Store the NPSSO code and set its expiration to 24 hours from now
    auth_data['npsso_code'] = npsso_code
    auth_data['expiration'] = datetime.now() + timedelta(hours=24)

    return jsonify(get_personal_info(cached_client))

# Middleware to check authentication before accessing other endpoints
@app.before_request
def check_authentication():
    global cached_client, psnawp, auth_data
    if request.endpoint != 'authenticate':  # Skip check for authentication route
        if not is_npsso_code_valid():
            return jsonify({"error": "Authentication expired. Please authenticate again."}), 401
        if cached_client is None:
            psnawp = PSNAWP(auth_data['npsso_code'])
            cached_client = psnawp.me()

# Other endpoints remain unchanged but will now check for authentication validity before proceeding

@app.route('/api/registered_devices', methods=['GET'])
def registered_devices():
    devices = get_registered_devices(cached_client)
    return jsonify(devices)

@app.route("/api/playing_time", methods=["GET"])
def get_playing_time():
    playing_time_data = []

    # Step 1: Check the database first
    db_data = get_playing_time_from_db()
    if db_data:
        for title in db_data:
            playing_time_data.append({
                'name': title[0],
                'play_count': title[1],
                'play_duration': title[2],
                'category': title[3],
                'first_played_date_time': title[4],
                'last_played_date_time': title[5],
                'image_url': title[6],
            })
        return jsonify(playing_time_data)

    # Step 2: If not in DB, fetch from PSN API
    titles_with_stats = cached_client.title_stats()

    for title in titles_with_stats:
        name = title.name
        play_count = title.play_count
        play_duration = str(title.play_duration)
        category = title.category.value
        first_played = str(title.first_played_date_time)
        last_played = str(title.last_played_date_time)
        image_url = title.image_url  # Assuming PSN API returns image_url

        # Insert into database
        insert_playing_time_into_db(name, play_count, play_duration, category, first_played, last_played,
                                    image_url)

        playing_time_data.append({
            'name': name,
            'play_count': play_count,
            'play_duration': play_duration,
            'category': category,
            'first_played_date_time': first_played,
            'last_played_date_time': last_played,
            'image_url': image_url,
        })

    return jsonify(playing_time_data)

# Force refresh endpoint
@app.route("/api/refresh_playing_time", methods=["POST"])
def refresh_playing_time():
    titles_with_stats = cached_client.title_stats()

    for title in titles_with_stats:
        name = title.name
        play_count = title.play_count
        play_duration = str(title.play_duration)
        category = title.category.value
        first_played = str(title.first_played_date_time)
        last_played = str(title.last_played_date_time)
        image_url = title.image_url  # Assuming PSN API returns image_url

        # Force update database
        insert_playing_time_into_db(name, play_count, play_duration, category, first_played, last_played,
                                    image_url)

    return jsonify({"message": "Data refreshed from PSN API"})

@app.route('/api/trophies_titles_list', methods=['GET'])
def trophies_titles_list():
    trophy_titles_list = trophy_titles(cached_client)
    return jsonify(trophy_titles_list)


@app.route('/api/user_info/<string:online_id>', methods=['GET'])
def user_info(online_id):
    user = get_user_info(psnawp, online_id)
    return jsonify(user)

@app.route('/api/search_game_titles', methods=['GET'])
def search_game_titles_API():
    search_query = request.args.get('query', '')
    search_results = search_game_titles(psnawp, search_query)
    return jsonify(search_results)

if __name__ == '__main__':
    app.run(debug=True)
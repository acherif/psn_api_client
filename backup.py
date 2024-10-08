
@app.route('/api/user_by_account_id/<string:account_id>', methods=['GET'])
def user_by_account_id(account_id):
    if cached_client is None:
        return jsonify({"error": "User information not cached. Please authenticate first."}), 400
    user = get_user_by_account_id(psnawp, account_id)
    return jsonify(user)

@app.route('/api/interact_group/<string:group_id>', methods=['GET'])
def interact_group(group_id):
    if cached_client is None:
        return jsonify({"error": "User information not cached. Please authenticate first."}), 400
    result = interact_with_group(psnawp, group_id)
    return jsonify(result)

@app.route('/api/create_group', methods=['POST'])
def create_group():
    user_online_ids = request.json.get('user_online_ids', [])
    users_list = [psnawp.user(online_id=user_id) for user_id in user_online_ids]
    new_group_info = create_new_group(psnawp, users_list)
    return jsonify(new_group_info)


@app.route('/api/friends_list', methods=['GET'])
def friends_list():
    if cached_client is None:
        return jsonify({"error": "User information not cached. Please authenticate first."}), 400
    friends = get_friends_list(cached_client)
    return jsonify(friends)

@app.route('/api/blocked_list', methods=['GET'])
def blocked_list():
    if cached_client is None:
        return jsonify({"error": "User information not cached. Please authenticate first."}), 400
    blocked = get_blocked_list(cached_client)
    return jsonify(blocked)

@app.route('/api/available_to_play', methods=['GET'])
def available_to_play():
    if cached_client is None:
        return jsonify({"error": "User information not cached. Please authenticate first."}), 400
    available = get_available_to_play(cached_client)
    return jsonify(available)

@app.route('/api/trophies/<string:title_id>', methods=['GET'])
def trophies(title_id):
    if cached_client is None:
        return jsonify({"error": "User information not cached. Please authenticate first."}), 400
    trophies_list = get_trophies(cached_client, title_id)
    return jsonify(trophies_list)

@app.route('/api/chat_groups', methods=['GET'])
def chat_groups():
    if cached_client is None:
        return jsonify({"error": "User information not cached. Please authenticate first."}), 400
    first_group_id, group_info_list = get_chat_groups(cached_client)
    return jsonify({"first_group_id": first_group_id, "group_info": group_info_list})

# @app.route('/api/playing_time', methods=['GET'])
# def playing_titles():
#     if cached_client is None:
#         return jsonify({"error": "User information not cached. Please authenticate first."}), 400
#     titles_with_stats = get_playing_time(cached_client)
#     return jsonify(titles_with_stats)

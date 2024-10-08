from psnawp_api import PSNAWP
from psnawp_api.models import SearchDomain
from psnawp_api.models.trophies import PlatformType

# Initialize PSNAWP globally
npsso_code = "<64 character npsso code>"  # Replace with your actual NPSSO code
psnawp = PSNAWP(npsso_code)

def get_personal_info(client):
    return {
        "online_id": client.online_id,
        "account_id": client.account_id,
        "profile": client.get_profile_legacy(),
    }

def initialize_psnawp(npsso_code):
    """Initialize PSNAWP with the given NPSSO code."""
    return PSNAWP(npsso_code)


def get_personal_info(client):
    """Fetch personal account info."""
    return {
        "online_id": client.online_id,
        "account_id": client.account_id,
        "profile": client.get_profile_legacy(),
    }


def get_registered_devices(client):
    """Fetch registered devices."""
    return [device for device in client.get_account_devices()]


def get_friends_list(client):
    """Fetch friends list."""
    return [friend for friend in client.friends_list()]


def get_blocked_list(client):
    """Fetch blocked users list."""
    return [blocked_user for blocked_user in client.blocked_list()]


def get_available_to_play(client):
    """Fetch users available to play."""
    return [user for user in client.available_to_play()]


def get_trophies(client, title_id):
    """Fetch trophies for a given title."""
    #trophies = client.trophy_summary()
    return [trophy for trophy in client.trophies(title_id, PlatformType.PS5)]



def trophy_titles(client):
    """Fetch trophies for a all titles."""
    return [trophy for trophy in client.trophy_titles()]

def get_chat_groups(client):
    """Fetch chat group information and return the first group's ID."""
    groups = client.get_groups()
    first_group_id = None
    group_info_list = []

    for id, group in enumerate(groups):
        if id == 0:  # Get the first group ID
            first_group_id = group.group_id
        group_info_list.append(group.get_group_information())

    return first_group_id, group_info_list


def get_playing_time(client):
    """Fetch playing time statistics."""
    return [
        {
            "name": title.name,
            "play_count": title.play_count,
            "title_id": title.title_id,
            "image_url": title.image_url,
            "category": title.category.value,
            "first_played_date_time": str(title.first_played_date_time),
            "last_played_date_time": str(title.last_played_date_time),
            "play_duration": str(title.play_duration)
        }
        for title in client.title_stats()
    ]

def get_user_info(psnawp, online_id):
    """Fetch information for a specific user by online ID."""
    user = psnawp.user(online_id=online_id)
    return {
        "online_id": user.online_id,
        "account_id": user.account_id,
        "profile": user.profile(),
        "prev_online_id": user.prev_online_id,
        "presence": user.get_presence(),
        "friendship": user.friendship(),
        "is_blocked": user.is_blocked(),
    }


def get_user_by_account_id(psnawp, account_id):
    """Fetch information for a specific user by account ID."""
    user = psnawp.user(account_id=account_id)
    return {"account_id": user.online_id}


def interact_with_group(psnawp, group_id):
    """Interact with a group using the group ID."""
    group = psnawp.group(group_id=group_id)
    group_info = group.get_group_information()
    conversation = group.get_conversation(10)  # Get the last 10 messages in the group
    return group_info, conversation


def create_new_group(psnawp, users_list):
    """Create and return a new group with specified users."""
    new_group = psnawp.group(users_list=users_list)
    return new_group.get_group_information()


def search_game_titles(psnawp, search_query):
    """Search for game titles based on a search query."""
    return [
        search_result["result"]["invariantName"]
        for search_result in psnawp.search(search_query=search_query, search_domain=SearchDomain.FULL_GAMES)
    ]


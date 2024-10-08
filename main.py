from psn_functions import *


def main():
    npsso_code = ""
    psnawp = initialize_psnawp(npsso_code)

    # Fetch and display personal account info
    client = psnawp.me()
    personal_info = get_personal_info(client)
    print(f"Personal Info: {personal_info}\n")

    # Fetch registered devices
    devices = get_registered_devices(client)
    print(f"Registered Devices: {devices}\n")

    titles_with_stats = client.title_stats()
    for title in titles_with_stats:
        print(
            f" \
            Game: {title.name} - \
            Title ID: {title.title_id} - \
            Play Count: {title.play_count} - \
            Play Duration: {title.play_duration} \n"
        )

    # Get trophies for a specific title (replace with actual title ID)
    trophies = get_trophies(client, "CUSA02126_00")
    print(f"Trophies: {trophies}\n")

    # Fetch playing time stats
    playing_time = get_playing_time(client)
    print(f"Playing Time Stats: {playing_time}\n")

    # Search for game titles
    search_results = search_game_titles(psnawp, search_query="GTA 5")
    print(f"Search Results: {search_results}\n")


if __name__ == "__main__":
    main()
"""
IMPORTANT: This only works with the spotify Extended Listening History JSON file!!!
"""

import json
from collections import Counter

DATA_PATH = 'Streaming_History_Audio_2024-2025.json' #CHANGE THIS TO YOUR FILE!


def get_top_five_artists(file_path, exclude_skipped=False, time_to_count=30000 ):
    """
    Gets the users top five favorite artists from a spotify JSON file. (excludes skipped songs)

    :param file_path: file path to spotify Extended Listening History JSON file
    :param exclude_skipped (optional): Exclude skipped songs from count of favorite artists (default: False)
    :param time_to_count (optional): Sets cut-off time for when a song shouldn't be counted as skip (default 30000 ms or 30 seconds)
    :return: list of users top five favorite artists
    """
    with open(file_path, 'r') as data_file:
        spotify_data = json.load(data_file)
    songs = []
    for song in spotify_data:
        if song['skipped'] == True and exclude_skipped and song['ms_played'] < 30000:
            continue
        else:
            songs.append(song['master_metadata_album_artist_name'])
    counted_artists = Counter(songs).most_common()
    return counted_artists[0],counted_artists[1],counted_artists[2],counted_artists[3],counted_artists[4]


    


    
    
    

    


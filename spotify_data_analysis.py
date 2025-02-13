"""
IMPORTANT: This only works with the spotify Extended Listening History JSON file!!!
"""

import datetime,json
from collections import Counter

DATA_PATH = 'Streaming_History_Audio_2024-2025.json' #CHANGE THIS TO YOUR FILE!


def get_top_five_artists(file_path, exclude_skipped=False, time_to_count=30000, data=None):
    """
    Gets the users top five favorite artists from a spotify JSON file. (excludes skipped songs)

    :param file_path: file path to spotify Extended Listening History JSON file
    :param exclude_skipped (optional): Exclude skipped songs from count of favorite artists (default: False)
    :param time_to_count (optional): Sets cut-off time for when a song shouldn't be counted as skip (default 30000 ms or 30 seconds)
    :param data (optional): overwrites the file path and instead uses the data passed into it HAS TO BE JSON
    :return: list of tuples of user's top five favorite artists and the amount of times they played a song from them
    """
    if data is None:
        with open(file_path, 'r') as data_file:
            spotify_data = json.load(data_file)
    else:
        spotify_data = data
    songs = []
    for song in spotify_data:
        if song['skipped'] == True and exclude_skipped and song['ms_played'] < time_to_count:
            continue
        else:
            songs.append(song['master_metadata_album_artist_name'])
    counted_artists = Counter(songs).most_common()
    if len(counted_artists) < 5:
        return counted_artists
    return counted_artists[0],counted_artists[1],counted_artists[2],counted_artists[3],counted_artists[4]

def create_date_range(start,end):
    """
    Returns a list of dates from the start date of the range to the end date of the range

    :param start: Start date (date object)
    :param end: End date (date object)
    :return: list of dates from start to end of range (date objects in list), returns -1 if invalid date range
    """
    if start > end:
        return -1
    
    date_list = []
    while start <= end:
        date_list.append(start)
        start += datetime.timedelta(days=1)
    return date_list

def get_songs_from_date_range(start,end):
    """
    Returns all the song objects from a certain range of dates

    :param start: Start 
    """
    pass



    


    
    
    

    


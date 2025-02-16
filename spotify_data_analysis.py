"""
IMPORTANT: This only works with the spotify Extended Listening History JSON file!!!
"""

import datetime
import json
from collections import Counter
from typing import Optional

DATA_PATH = (
    "Streaming_History_Audio_2024-2025.json"  # CHANGE THIS TO YOUR FILE!
)


def get_total_time_listened(file_path: Optional[str]=None, data: Optional[list] = None) -> tuple:
    """
    Gets the total amount of time the user listened to music.

    :param str file_path: The path to the file
    :param list data: overwrites file_path, using the data passed in instead
    :rtype: tuple
    :returns: A tuple containing how many ms, seconds, minutes, hours, days, weeks, months, and years music was playing for
    """
    if file_path is None and data is None:
        print("Neither arguments are fulfilled")
        raise TypeError("Positional arguments not passed!")
    total_ms_listened = 0
    if data is None:
        try:
            with open(file_path) as data_file:
                spotify_data = json.load(data_file)
        except FileNotFoundError:
            print(f"File {file_path} could not be found!")
            return -1
        except json.JSONDecodeError:
            print(f"Invalid JSON")
            return -1
    else:
        spotify_data = data
    
    for song in spotify_data:
        total_ms_listened += song['ms_played']

    seconds = total_ms_listened/1000
    minutes = seconds/60
    hours = minutes/60
    days = hours/24
    weeks = days/7
    months = weeks/4
    years = months/12
    return total_ms_listened, round(seconds,4), round(minutes,4), round(hours,4), round(days,4), round(weeks,4), round(months,4), round(years,4)




def get_top_five_artists(
    exclude_skipped: Optional[bool], time_to_count: Optional[int] = 30000, data: Optional[list]=None,file_path: Optional[str]=None
) -> tuple:
    """
    Gets the users top five favorite artists from a spotify JSON file. (excludes skipped songs)

    :param str file_path: file path to spotify Extended Listening History JSON file
    :param bool exclude_skipped (optional): Exclude skipped songs from count of favorite artists (default: False)
    :param int time_to_count (optional): Sets cut-off time for when a song shouldn't be counted as skip (default 30000 ms or 30 seconds)
    :param list data (optional): overwrites the file path and instead uses the data passed into it
    :rtype: tuple
    :return: list of tuples of user's top five favorite artists and the amount of times they played a song from them
    """
    if file_path is None and data is None:
        print("Neither arguments are fulfilled")
        raise TypeError("Positional arguments not passed!")
    if data is None:
        try:
            with open(file_path, "r") as data_file:
                spotify_data = json.load(data_file)
        except FileNotFoundError:
            print(f"File {file_path} not found!")
            return -1
        except json.JSONDecodeError:
            print(
                f"File {file_path} could not be decoded! Check for invalid JSON?"
            )
            return -1

    else:
        spotify_data = data
    songs = []
    for song in spotify_data:
        if (
            song["skipped"] is True
            and exclude_skipped
            and song["ms_played"] < time_to_count
        ):
            continue
        else:
            songs.append(song["master_metadata_album_artist_name"])
    counted_artists = Counter(songs).most_common()
    if len(counted_artists) < 5:
        return tuple(counted_artists)
    return (
        counted_artists[0],
        counted_artists[1],
        counted_artists[2],
        counted_artists[3],
        counted_artists[4],
    )


def create_date_range(start: datetime.datetime, end: datetime.datetime) -> list:
    """
    Returns a list of dates from the start date of the range to the end date of the range

    :param datetime.datetime start: Start date (date object)
    :param datetime.datetime end: End date (date object)
    :rtype: list
    :return: list of dates from start to end of range (date objects in list), returns -1 if invalid date range
    """
    if start > end:
        return -1

    date_list = []
    while start <= end:
        date_list.append(start)
        start += datetime.timedelta(days=1)
    return date_list


def get_songs_from_date_range(start: datetime.datetime, end: datetime.datetime,filepath: Optional[str]= None,data: Optional[list] = None) -> list:
    """
    Returns all the song objects from a certain range of dates

    :param list data: JSON data, overrides filepath (optional)
    :param str filepath: filepath to data 
    :param datetime.datetime start: Start date of range (datetime object)
    :param datetime.datetime end: End date of range (datetime object)
    """
    if filepath is None and data is None:
        print("Neither arguments are fulfilled")
        raise TypeError("Positional arguments not passed!")
    songs = []
    date_range = create_date_range(start, end)
    if data is None:
        try:
            with open(filepath, mode="r") as spotify_data_file:
                spotify_data = json.load(spotify_data_file)
        except FileNotFoundError:
            print(f"File {filepath} not found!")
        except json.JSONDecodeError:
            print(f"Invalid json in file {filepath}")

    for song in spotify_data:
        if (
            datetime.datetime.strptime(song["ts"][:10], "%Y-%m-%d")
            in date_range
        ):
            songs.append(song)
    return songs

def get_most_listened_to_song(filepath: Optional[str] = None, data: Optional[list] = None) -> str:
    """
    returns the users most listened to song.

    :param str filepath: filepath to data
    :param list data: optional data to overwrite filepath
    :rtype: str
    :returns: users most listened to song (Song name - Artist)
    """
    if filepath is None and data is None:
        print("Neither arguments are fulfilled")
        raise TypeError("Positional arguments not passed!")
    if data is None:
        try:
            with open(filepath,'r') as spotify_data_file:
                spotify_data = json.load(spotify_data_file)
        except FileNotFoundError:
            print(f"File {filepath} not found!")
            return -1
        except json.JSONDecodeError: 
            print(f"File {filepath} could not be decoded.")
            return -1
    else:
        spotify_data = data
    
    songs = []
    for song in spotify_data:
        songs.append((song['master_metadata_track_name'], song['master_metadata_album_artist_name']))
    
    most_common = Counter(songs).most_common()[0]
    
    return f'{most_common[0][0]} - {most_common[0][1]}'

def get_most_listened_to_album(filepath: Optional[str] = None, data: Optional[str] = None) -> str:
    """
    Returns users most listened to album

    :param filepath: filepath to JSON file.
    :param data: overwrites filepath data and uses that data instead
    """
    if filepath is None and data is None:
        print("Neither arguments are fulfilled")
        raise TypeError("Positional arguments not passed!")
    if data is None:
        with open(filepath, 'r') as spotify_data_file:
            spotify_data = json.load(spotify_data_file)
    else:
        spotify_data = data

    albums = [song['master_metadata_album_album_name'] for song in spotify_data]

    return Counter(albums).most_common()[0][0]




    




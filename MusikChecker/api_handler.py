# api_handler.py

import musicbrainzngs
import Levenshtein
import re
import datetime

# Set the user agent as required by MusicBrainz.
musicbrainzngs.set_useragent("MyMusicCheckerApp", "1.0", "michaeldengl@hotmail.com")

def clean_album_name(name, band_name=None, remove_special=False):
    """
    Cleans the album name by:
      - Removing extraneous text in parentheses and brackets.
      - Removing any year numbers (in YYYY or YY format) from 1950 until the current year.
      - Removing any occurrence of a number followed by "kbps" or "kpbs".
      - Removing the band name (if provided) from the album name.
      - Normalizing whitespace.
      - Optionally removing all non-alphanumeric characters.
    
    Args:
        name (str): The original album name.
        band_name (str, optional): The band name to remove if present.
        remove_special (bool, optional): If True, removes all non-alphanumeric characters.
    
    Returns:
        str: The cleaned album name in lowercase.
    """
    # Remove any text in parentheses and brackets.
    name = re.sub(r"\s*\([^)]*\)", "", name)
    name = re.sub(r"\s*\[[^]]*\]", "", name)
    
    # Remove any year numbers from 1950 until the current year.
    current_year = datetime.datetime.now().year
    def remove_year(match):
        token = match.group(0)
        try:
            num = int(token)
        except ValueError:
            return token
        # For four-digit numbers (YYYY)
        if len(token) == 4 and 1950 <= num <= current_year:
            return ""
        # For two-digit numbers (YY)
        elif len(token) == 2:
            last_two = current_year % 100
            if (50 <= num <= 99) or (0 <= num <= last_two):
                return ""
        return token

    name = re.sub(r"\b\d{2,4}\b", remove_year, name)
    
    # Remove any number followed by "kbps" or "kpbs" (case-insensitive).
    name = re.sub(r"\b\d+\s*k(?:bps|pbs)\b", "", name, flags=re.IGNORECASE)
    
    # Remove the band name (case-insensitive), if provided.
    if band_name:
        name = re.sub(re.escape(band_name), "", name, flags=re.IGNORECASE)
    
    # Normalize extra whitespace.
    name = re.sub(r"\s+", " ", name)
    name = name.strip()
    
    if remove_special:
        name = re.sub(r"[^A-Za-z0-9]", "", name)
    
    return name.lower()

def best_album_match(local_album, online_album_titles, band_name, threshold_ratio=0.8):
    """
    Compares the provided local album name (after cleaning) against a set of online album titles,
    using the Levenshtein similarity ratio.
    
    Args:
        local_album (str): The local album name.
        online_album_titles (iterable): An iterable of album titles (strings) to compare against.
        band_name (str): The band name to remove during cleaning.
        threshold_ratio (float): Minimum similarity ratio required for a match.
    
    Returns:
        tuple: (best_match, best_ratio) where best_match is the best online title found or None.
    """
    best_match = None
    best_ratio = 0.0
    cleaned_local = clean_album_name(local_album, band_name).lower()
    
    for album in online_album_titles:
        cleaned_online = clean_album_name(album, band_name).lower()
        ratio = Levenshtein.ratio(cleaned_local, cleaned_online)
        print(f"Matching '{cleaned_local}' vs '{cleaned_online}' with similarity ratio = {ratio}")
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = album
    if best_ratio >= threshold_ratio:
        return best_match, best_ratio
    else:
        return None, best_ratio

def get_online_albums(band_name, limit=5):
    """
    Searches for the given band using MusicBrainz, selects the best matching artist using Levenshtein distance,
    and retrieves a dictionary of album titles to their first-release year (if available).
    
    Only release groups with a primary type of "Album" and no secondary types are considered.
    
    Args:
        band_name (str): The name of the band.
        limit (int): The maximum number of artist search results to consider.
        
    Returns:
        dict: A dictionary mapping album titles (str) to first-release year (str, possibly empty).
              For example: { "An Awesome Wave": "2012", ... }
    """
    try:
        result = musicbrainzngs.search_artists(artist=band_name, limit=limit)
        artist_list = result.get('artist-list', [])
        if not artist_list:
            print(f"No artists found for '{band_name}'.")
            return {}
        
        best_artist = None
        best_distance = float('inf')
        for artist in artist_list:
            candidate_name = artist.get('name', '')
            distance = Levenshtein.distance(band_name.lower(), candidate_name.lower())
            print(f"Comparing '{band_name}' with '{candidate_name}'; distance = {distance}")
            if distance < best_distance:
                best_distance = distance
                best_artist = artist
        
        if best_artist is None:
            print(f"No suitable artist match found for '{band_name}'.")
            return {}
        
        artist_id = best_artist.get('id')
        print(f"Best match for '{band_name}' is '{best_artist.get('name')}' with ID: {artist_id}")
        
        # Retrieve release groups for the artist.
        release_groups = musicbrainzngs.browse_release_groups(artist=artist_id, limit=100)
        album_dict = {}
        for rg in release_groups.get('release-group-list', []):
            primary_type = rg.get('primary-type', '')
            if primary_type.lower() == "album":
                title = rg.get('title')
                # Only include if there are no secondary types.
                if title and not rg.get('secondary-type-list', []):
                    first_release_date = rg.get('first-release-date', '')
                    if first_release_date:
                        year = first_release_date[:4]
                    else:
                        year = ""
                    album_dict[title] = year
        return album_dict
    
    except Exception as e:
        print(f"Error retrieving data for '{band_name}': {e}")
        return {}

def get_best_album_match(band_name, local_album, limit=5, threshold_ratio=0.8):
    """
    Retrieves the online album dictionary for a band and uses fuzzy matching to select the best match for a local album.
    
    Args:
        band_name (str): The band for which to retrieve album data.
        local_album (str): The local album title.
        limit (int): The maximum number of artist search results to consider.
        threshold_ratio (float): The minimum similarity ratio for a valid match.
        
    Returns:
        str or None: The matching online album title, if found.
    """
    online_album_dict = get_online_albums(band_name, limit=limit)
    if not online_album_dict:
        return None
    match, ratio = best_album_match(local_album, online_album_dict.keys(), band_name, threshold_ratio)
    if match:
        print(f"Match found for '{local_album}': '{match}' (similarity ratio: {ratio})")
    else:
        print(f"No close match found for '{local_album}'. Best ratio: {ratio}")
    return match
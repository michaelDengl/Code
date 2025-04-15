# api_handler.py

import musicbrainzngs
import Levenshtein
import re

# Set the user agent as required by MusicBrainz.
musicbrainzngs.set_useragent("MyMusicCheckerApp", "1.0", "michaeldengl@hotmail.com")

def clean_album_name(name, band_name=None):
    """
    Cleans the album name by:
      - Removing extraneous text in parentheses and brackets.
      - Removing the band name (if provided) from the album name.
      - Normalizing whitespace.
    
    For example:
      "An Awesome Wave (2012)"  becomes "An Awesome Wave"
      "alt-j - This Is All Yours (2014) CD RIP [MP3 @ 320 KBPS]" 
              becomes "This Is All Yours"
    
    Args:
        name (str): The original album name.
        band_name (str, optional): The band name to remove if present.
    
    Returns:
        str: The cleaned album name.
    """
    # Remove any text in parentheses and brackets.
    name = re.sub(r"\s*\([^)]*\)", "", name)
    name = re.sub(r"\s*\[[^]]*\]", "", name)
    # Remove the band name (case-insensitive), if provided.
    if band_name:
        name = re.sub(re.escape(band_name), "", name, flags=re.IGNORECASE)
    # Normalize extra whitespace.
    name = re.sub(r"\s+", " ", name)
    return name.strip()

def best_album_match(local_album, online_albums, band_name, threshold_ratio=0.8):
    """
    Compares the provided local album name (after cleaning) against a set of online album names,
    also cleaned, using the Levenshtein similarity ratio.
    
    Args:
        local_album (str): The album name from the local system.
        online_albums (iterable): A set or list of album names retrieved online.
        band_name (str): The band name to remove from both local and online titles.
        threshold_ratio (float): Minimum similarity ratio required for a match.
        
    Returns:
        tuple: (best_match, best_ratio) where best_match is the online album title
               that best matches the local_album, or None if no match exceeds the threshold.
    """
    best_match = None
    best_ratio = 0.0
    # Clean and lower the local album name for comparison.
    cleaned_local = clean_album_name(local_album, band_name).lower()
    
    for album in online_albums:
        # Clean and lower each online album name, also removing the band name.
        cleaned_online = clean_album_name(album, band_name).lower()
        # Compute similarity ratio.
        ratio = Levenshtein.ratio(cleaned_local, cleaned_online)
        print(f"Matching '{cleaned_local}' vs '{cleaned_online}' with similarity ratio = {ratio}")
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = album
    # Only accept a match if it meets or exceeds the threshold.
    if best_ratio >= threshold_ratio:
        return best_match, best_ratio
    else:
        return None, best_ratio

def get_online_albums(band_name, limit=5):
    """
    Searches for the given band using MusicBrainz, selects the best matching artist using Levenshtein distance,
    and retrieves a set of album titles (official albums only) for that artist.
    
    The function uses browse_release_groups to get all release groups for the artist and then
    filters them manually to include only those with "primary-type" equal to "Album".
    
    Args:
        band_name (str): The name of the band.
        limit (int): The maximum number of search results to consider.
        
    Returns:
        set: A set of album titles (official albums) found online.
    """
    try:
        # Search for artists matching the provided band name.
        result = musicbrainzngs.search_artists(artist=band_name, limit=limit)
        artist_list = result.get('artist-list', [])
        
        if not artist_list:
            print(f"No artists found for '{band_name}'.")
            return set()
        
        # Select the best matching artist based on Levenshtein distance.
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
            return set()
        
        artist_id = best_artist.get('id')
        print(f"Best match for '{band_name}' is '{best_artist.get('name')}' with ID: {artist_id}")
        
        # Retrieve all release groups for the artist.
        release_groups = musicbrainzngs.browse_release_groups(artist=artist_id, limit=100)
        album_names = set()
        # Filter release groups to include only those with a primary type of "Album".
        for rg in release_groups.get('release-group-list', []):
            primary_type = rg.get('primary-type', '')
            if primary_type.lower() == "album":
                title = rg.get('title')
                if title:
                    album_names.add(title)
        return album_names
    
    except Exception as e:
        print(f"Error retrieving data for '{band_name}': {e}")
        return set()

def get_best_album_match(band_name, local_album, limit=5, threshold_ratio=0.8):
    """
    Retrieves the online album list for a band and uses fuzzy matching (after cleaning both local and online album names)
    to select the best match for a given local album title. The cleaning process also removes the band name from the titles.
    
    Args:
        band_name (str): The band for which to retrieve album data.
        local_album (str): The local album title that might contain extraneous data and the band name.
        limit (int): The maximum number of artist search results to consider.
        threshold_ratio (float): The minimum similarity ratio for a valid match.
        
    Returns:
        str or None: The online album title that best matches the local_album, or None if no match meets the threshold.
    """
    online_albums = get_online_albums(band_name, limit=limit)
    if not online_albums:
        return None
    match, ratio = best_album_match(local_album, online_albums, band_name, threshold_ratio)
    if match:
        print(f"Match found for '{local_album}': '{match}' (similarity ratio: {ratio})")
    else:
        print(f"No close match found for '{local_album}'. Best ratio: {ratio}")
    return match

# folder_scanner.py

import os

def scan_music_directory(root_dir):
    """
    Walks through the given root folder recursively.
    Assumes the first level is a band and the second level contains albums.
    Returns a dictionary with bands as keys and a list of albums as values.
    """
    music_data = {}
    # Walk through the directory tree.
    for dirpath, dirnames, filenames in os.walk(root_dir):
        rel_path = os.path.relpath(dirpath, root_dir)
        parts = rel_path.split(os.sep)
        
        # If we're at the band level (directly under the root)
        if len(parts) == 1 and parts[0] != '.':
            band = parts[0]
            if band not in music_data:
                music_data[band] = {'albums': []}
        # If we're at the album level (subfolder within a band folder)
        elif len(parts) == 2:
            band, album = parts
            if band in music_data:
                music_data[band]['albums'].append(album)
    return music_data

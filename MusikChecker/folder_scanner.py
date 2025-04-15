#!/usr/bin/env python
"""
folder_scanner.py

Scans the local music folder structure and returns a dictionary mapping each band (first-level folder)
to a list of album names. This version supports both:
  - Albums that exist directly under the band folder (band -> album)
  - Albums that exist in any subfolder within the band folder (band -> any_folder -> album)

Any folders deeper than level 3 (i.e., more than one subfolder under the band folder) are ignored.
"""

import os

def scan_music_directory(root_dir):
    """
    Walks through the given root folder recursively and constructs a dictionary where keys are band names
    and values are dictionaries containing a list of album names under the key 'albums'. This function captures:
      - Albums directly under the band folder (e.g., band/AlbumName, depth == 2)
      - Albums located one level below a grouping folder inside the band folder 
        (e.g., band/some_group/AlbumName, depth == 3)

    Args:
        root_dir (str): The absolute (or relative) path to your root music folder.

    Returns:
        dict: A dictionary mapping each band to its albums.
              Example:
              {
                "BandName": { "albums": ["Album1", "Album2", ...] },
                ...
              }
    """
    music_data = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Get the path relative to the root directory.
        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path == '.':
            # Skip the root folder itself.
            continue

        # Split the path into components.
        parts = rel_path.split(os.sep)
        # The first part is always treated as the band name.
        band = parts[0]
        if band not in music_data:
            music_data[band] = {"albums": []}

        # If the structure is "band/album" (depth == 2), add the album folder.
        if len(parts) == 2:
            album = parts[1]
            if album not in music_data[band]["albums"]:
                music_data[band]["albums"].append(album)
        # If the structure is "band/any_folder/album" (depth == 3), use the subfolder as the album name.
        elif len(parts) == 3:
            album = parts[2]
            if album not in music_data[band]["albums"]:
                music_data[band]["albums"].append(album)
        # Folders deeper than level 3 are ignored.

    return music_data
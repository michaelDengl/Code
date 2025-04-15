# main.py

from config import ROOT_DIR, REPORT_FILE  # REPORT_FILE is the text report path.
from folder_scanner import scan_music_directory
from api_handler import get_best_album_match, get_online_albums
from report_generator import generate_text_report
from report_excel import generate_excel_report

def main():
    print("Scanning local music directory...")
    local_music = scan_music_directory(ROOT_DIR)
    
    report = {}
    # Process each band and its albums.
    for band, data in local_music.items():
        album_matches = {}
        print(f"\nProcessing band: {band}")
        # Retrieve the full set of online albums for this band.
        online_albums = get_online_albums(band)
        
        # For each local album, get the best matching online album.
        for album in data['albums']:
            print(f"Checking local album: {album}")
            best_match = get_best_album_match(band, album)
            album_matches[album] = best_match
        
        # Build a set of matched online album titles.
        matched_online_set = set(match for match in album_matches.values() if match)
        # Determine which online albums are missing locally.
        missing_local = online_albums - matched_online_set
        
        report[band] = {
            "album_matches": album_matches,
            "missing_local": sorted(list(missing_local))
        }
    
    # Generate a text report.
    generate_text_report(report, REPORT_FILE)
    
    # Define an Excel report filename (you can add this to config.py if you wish).
    excel_report_file = REPORT_FILE.replace('.txt', '.xlsx')
    # Generate an Excel report.
    generate_excel_report(report, excel_report_file)

if __name__ == "__main__":
    main()

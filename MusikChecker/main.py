from config import ROOT_DIR, REPORT_FILE
from folder_scanner import scan_music_directory
from api_handler import get_best_album_match, get_online_albums
from report_generator import generate_text_report
from report_excel import generate_excel_report

def main():
    print("Scanning local music directory...")
    local_music = scan_music_directory(ROOT_DIR)
    
    report = {}
    
    for band, data in local_music.items():
        album_matches = {}
        print(f"\nProcessing band: {band}")
        # Retrieve the online album dictionary for this band.
        online_album_dict = get_online_albums(band)
        
        # For each local album, find the best online match.
        for album in data['albums']:
            print(f"Checking local album: {album}")
            best_match = get_best_album_match(band, album)
            album_matches[album] = best_match
        
        # Get the set of matched online album titles.
        matched_online_set = set(match for match in album_matches.values() if match)
        # Determine which online albums are missing locally.
        missing_local = set(online_album_dict.keys()) - matched_online_set
        
        # Annotate missing albums with their year (if available).
        missing_local_with_year = []
        for online_album in missing_local:
            year = online_album_dict.get(online_album, "")
            if year:
                missing_local_with_year.append(f"{year} - {online_album}")
            else:
                missing_local_with_year.append(online_album)
        
        report[band] = {
            "album_matches": album_matches,
            "missing_local": sorted(list(missing_local_with_year))
        }
    
    # Generate a text report.
    generate_text_report(report, REPORT_FILE)
    
    # Generate an Excel report (Excel file name derived from REPORT_FILE).
    excel_report_file = REPORT_FILE.replace('.txt', '.xlsx')
    generate_excel_report(report, excel_report_file)

if __name__ == "__main__":
    main()

# report_generator.py

def generate_text_report(report_data, output_file):
    """
    Creates a text report summarizing:
      - The album matches (local album -> online album).
      - The online albums that are missing locally.
    
    Args:
        report_data (dict): Should be structured as:
            {
                band: {
                    "album_matches": { local_album: online_match, ... },
                    "missing_local": [ online_album1, online_album2, ... ]
                },
                ...
            }
        output_file (str): Path to the output text file.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for band, details in report_data.items():
            f.write(f"Band: {band}\n")
            f.write("Album Matches:\n")
            for local_album, online_match in details["album_matches"].items():
                if online_match:
                    f.write(f"  - {local_album}  ->  {online_match}\n")
                else:
                    f.write(f"  - {local_album}  ->  No online match found\n")
            f.write("Missing Locally (present online but not found locally):\n")
            if details["missing_local"]:
                for missing in details["missing_local"]:
                    f.write(f"  - {missing}\n")
            else:
                f.write("  None\n")
            f.write("\n")
    print(f"Report generated: {output_file}")

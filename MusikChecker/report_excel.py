import pandas as pd

def generate_excel_report(report_data, output_file):
    """
    Creates an Excel report with two sheets:
      - "Album Matches": Shows, for each band, the local album and the best matching online album.
      - "Missing Online": Shows, for each band, the online albums that were not matched locally.
    
    Args:
        report_data (dict): Structured as:
            {
                band: {
                    "album_matches": { local_album: online_match, ... },
                    "missing_local": [ online_album1, online_album2, ... ]
                },
                ...
            }
        output_file (str): Path to the Excel output file.
    """
    # Build DataFrame for album matches.
    match_rows = []
    for band, details in report_data.items():
        album_matches = details.get("album_matches", {})
        for local_album, online_match in album_matches.items():
            match_rows.append({
                'Band': band,
                'Local Album': local_album,
                'Online Match': online_match if online_match is not None else "No online match"
            })
    if match_rows:
        df_matches = pd.DataFrame(match_rows)
        df_matches = df_matches.sort_values(by=['Band', 'Local Album'])
    else:
        # Create an empty DataFrame with the proper columns.
        df_matches = pd.DataFrame(columns=['Band', 'Local Album', 'Online Match'])
    
    # Build DataFrame for online albums missing locally.
    missing_rows = []
    for band, details in report_data.items():
        missing = details.get("missing_local", [])
        if missing:
            for album in missing:
                missing_rows.append({
                    'Band': band,
                    'Missing Online Album': album
                })
        else:
            missing_rows.append({
                'Band': band,
                'Missing Online Album': "None"
            })
    if missing_rows:
        df_missing = pd.DataFrame(missing_rows)
        df_missing = df_missing.sort_values(by=['Band'])
    else:
        df_missing = pd.DataFrame(columns=['Band', 'Missing Online Album'])
    
    # Write both DataFrames to an Excel file in separate sheets.
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df_matches.to_excel(writer, sheet_name="Album Matches", index=False)
        df_missing.to_excel(writer, sheet_name="Missing Online", index=False)
    
    print(f"Excel report generated: {output_file}")

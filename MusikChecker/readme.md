# Music Checker Program

This is a Python program that scans your local music collection (organized by artist and album folders), queries the MusicBrainz database for official album release information, performs fuzzy matching (using Levenshtein distance) between your local album names and the online records, and generates detailed reports. It produces both a text report and an Excel report.

## Features

- **Local Directory Scanning:**  
  Recursively scans a specified root folder containing artist subdirectories and album subdirectories to build a list of local albums.

- **MusicBrainz Integration:**  
  Uses the `musicbrainzngs` library to query the MusicBrainz API for online album data and filters the results to include only official album release groups.

- **Fuzzy Matching:**  
  Utilizes the `python-Levenshtein` library to perform fuzzy matching between local album titles and online album titles. Cleaning functions remove extraneous details (such as year, format info, or even the artist name) for more accurate matching.

- **Report Generation:**  
  Produces two types of reports:
  - **Text Report:** A simple report that lists album matches (local album → online album) and shows which online albums are missing locally.
  - **Excel Report:** A polished, multi-sheet report (using Pandas and XlsxWriter) that contains one sheet for album matches and another for online albums missing from your local collection.


## Requirements

The project requires Python 3 and the following Python packages:

- `musicbrainzngs`
- `python-Levenshtein`
- `pandas`
- `XlsxWriter`

Install the dependencies by running:

```bash
pip install -r requirements.txt


## Acknowledgements

The MusicBrainz community for their extensive music database.

The developers of the Python packages musicbrainzngs, python-Levenshtein, pandas, and XlsxWriter for making this project possible.

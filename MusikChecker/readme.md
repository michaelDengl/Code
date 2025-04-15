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

## Project Structure

music_checker/
├── api_handler.py        # Functions for querying MusicBrainz and performing fuzzy matching.
├── config.py             # Configuration file with paths and settings.
├── folder_scanner.py     # Scans the local folder structure to extract artist and album data.
├── main.py               # Main script that coordinates scanning, matching, and report generation.
├── report_generator.py   # Generates a text-based report.
├── report_excel.py       # Generates an Excel report using Pandas.
└── requirements.txt      # Lists the required Python packages.



## Requirements

The project requires Python 3 and the following Python packages:

- `musicbrainzngs`
- `python-Levenshtein`
- `pandas`
- `XlsxWriter`

Install the dependencies by running:

pip install -r requirements.txt


## Setup and Usage

1. **Configure Your Environment:**

- `Edit config.py to update the ROOT_DIR variable with the path to your local music folder.`

- `Optionally adjust output file names for your reports (REPORT_FILE for the text report; the Excel file name can be defined or generated` automatically).

2. **Run the Program:**

Execute the main script from your terminal:

**python main.py**
The program will:

- `Scan your local music folders.`

- `Query MusicBrainz to retrieve official album data for each artist.`

- `Use fuzzy matching to compare your local album names with the online records.`

- `Generate both a text report and an Excel report containing:`

  - `Album Matches: Mapping of local album names to the best matching online album names.`

  - `Missing Online Albums: A list of online albums that are missing from your local collection.`

3. **View the Reports:**

- `Open the text file (e.g., music_report.txt) to view a simple report.`

- `Open the Excel file (e.g., music_report.xlsx) for a detailed, sortable report with two sheets.`


## How It Works
- **Local Scanning:**
The folder_scanner.py script recursively processes your local music folder and creates a mapping of each artist to their albums.

- **API Query & Matching:**
The api_handler.py script handles the MusicBrainz API requests. It retrieves official album release groups (by filtering release groups with a primary type of Album) and applies fuzzy matching using Levenshtein distance after cleaning up the album names.

- **Report Generation:**

- **report_generator.py** creates a plain-text report.

- **report_excel.py** uses **Pandas to** create an Excel workbook with two sheets:

  - **Album Matches:** Local album versus best online match.

  - **Missing Online:** Online albums not found locally.

## Future Improvements
- `Enhance the fuzzy matching algorithm for even better accuracy.`

- `Improve the cleaning routines to handle more variations in album naming.`

- `Add command-line options or a GUI for easier customization.`

- `Implement additional filtering based on release year or type.`

## Acknowledgements
- `The MusicBrainz community for their extensive music database.`

- `The developers of the Python packages musicbrainzngs, python-Levenshtein, pandas, and XlsxWriter for making this project possible.`
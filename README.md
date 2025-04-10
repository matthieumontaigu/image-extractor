# Image extractor

A Python-based utility to fetch high-quality movie posters from Apple TV and iTunes. The tool supports scraping web pages and interacting with APIs to retrieve movie poster URLs.

## Features
- Extract movie poster URLs from Apple TV pages.
- Search and retrieve iTunes movie posters using the iTunes API.
- Handles complex URL cleaning and parsing.
- Modular design for easy extensibility and maintenance.

## Requirements
- Python 3.10 or higher
- Google Chrome and ChromeDriver (for optional Selenium interactions)

## Installation
1. Clone the Repository:
```bash
git clone https://github.com/matthieumontaigu/image-extractor.git
cd image-extractor
```

2. Create a Virtual Environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install Dependencies:
```bash
pip install -r requirements.txt
```
4. Install ChromeDriver:
    - Download ChromeDriver from here based on your Chrome version.
    - Ensure ChromeDriver is in your system’s PATH or place it in the repository root.

## Usage

### Extract

Run the tool using the main.py script to extract movie poster:
```bash
python main.py extract --url <URL>
```

#### Example
```bash
python main.py extract --url "https://tv.apple.com/movie/some-movie-url"
```

The tool will extract and display the high-resolution movie poster URL for the provided Apple TV or iTunes movie link.

#### Thumbnail
```bash
python main.py extract --url "https://tv.apple.com/movie/some-movie-url" --thumbnail --use-selenium
```
It is possible to extract thumbnail as an option. As it requires to dynamically navigate though the page, selenium is needed.
If you do not support selenium, a fallback based on requests is implemented, just remove the flag.

### Search
You can also look for the 10 best matches in the iTunes Store API, for any movie name.
```bash
python main.py search --country <COUNTRY> --term <TERM>
```

#### Example
```bash
python main.py search --country "us" --term "titanic"
```

## Directory Structure

```plaintext
image-extractor/
├── main.py                  # Entry point for the application
├── utils/                   # Helper functions for common tasks
│   ├── url_helpers.py       # URL parsing and validation
│   ├── selenium_helpers.py  # Selenium WebDriver setup and interaction
│   ├── request_helpers.py   # HTTP requests
│   ├── parsing_helpers.py   # BeautifulSoup HTML parsing
│   └── print_helpers.py     # Printing utilities
├── services/
│   ├── apple_tv/            # Apple TV scraping logic
│   │   ├── extract.py       # Extract artwork URLs
│   │   ├── background.py    # Background image extraction
│   │   ├── logo.py          # Logo image extraction
│   │   ├── thumbnail.py     # Thumbnail image extraction
│   │   └── utils.py         # Apple TV-specific utilities
│   ├── itunes/              # iTunes API interaction
│   │   ├── extract.py       # Extract artwork URLs
│   │   └── search.py        # Search movies in iTunes
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
└── .gitignore               # Git ignored files
```


## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (git checkout -b feature/new-feature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/new-feature).
5. Open a pull request.

## Acknowledgments
- BeautifulSoup for HTML parsing.
- Selenium for web automation.
- Requests for HTTP requests.
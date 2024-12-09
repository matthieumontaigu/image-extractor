# Image extractor

A Python-based utility to fetch high-quality movie posters from Apple TV and iTunes. The tool supports scraping web pages and interacting with APIs to retrieve movie poster URLs.

## Features
- Extract movie poster URLs from Apple TV pages.
- Search and retrieve iTunes movie posters using the iTunes API.
- Handles complex URL cleaning and parsing.
- Modular design for easy extensibility and maintenance.

## Requirements
- Python 3.8 or higher
- Google Chrome and ChromeDriver (for Selenium interactions)

## Installation
1. Clone the Repository:
```bash
git clone https://github.com/your-username/movie-poster-tool.git
cd movie-poster-tool
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

Run the tool using the main.py script:
```bash
python main.py <URL>
```

### Example:
```bash
python src/main.py "https://tv.apple.com/movie/some-movie-url"
```

The tool will extract and display the high-resolution movie poster URL for the provided Apple TV or iTunes movie link.

## Directory Structure

```plaintext
movie_poster_tool/
├── main.py                  # Entry point for the application
├── utils/                   # Helper functions for common tasks
│   ├── url_helpers.py       # URL parsing and validation
│   ├── selenium_helpers.py  # Selenium WebDriver setup and interaction
│   ├── request_helpers.py   # HTTP requests
│   ├── parsing_helpers.py   # BeautifulSoup HTML parsing
└── services/                # Business logic for external services
│   ├── apple_tv_service.py  # Apple TV scraping logic
│   ├── itunes_service.py    # iTunes API interaction
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── LICENSE                      # License file
└── .gitignore                   # Git ignored files
```


## Contributing

Contributions are welcome! To contribute:
	1.	Fork the repository.
	2.	Create a new branch (git checkout -b feature/new-feature).
	3.	Commit your changes (git commit -m 'Add some feature').
	4.	Push to the branch (git push origin feature/new-feature).
	5.	Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
	•	BeautifulSoup for HTML parsing.
	•	Selenium for web automation.
	•	Requests for HTTP requests.
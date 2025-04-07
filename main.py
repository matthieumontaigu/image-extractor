import argparse

from services.apple_tv.extract import extract_artworks
from services.itunes.extract import extract_artwork, get_artworks
from utils.print_helpers import print_artworks, print_search_results
from utils.url_helpers import clean_url, extract_domain, get_movie_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch movie posters")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    extract_parser = subparsers.add_parser(
        "extract", help="Get movie poster URL from Apple TV and iTunes"
    )
    extract_parser.add_argument("--url", help="URL of the movie")
    extract_parser.add_argument(
        "--thumbnail",
        action="store_true",
        help="Get the thumbnail image of the movie",
    )
    extract_parser.add_argument(
        "--use-selenium",
        action="store_true",
        help="Authorize the usage of selenium library to extend scrapping capabilities",
    )

    search_parser = subparsers.add_parser(
        "search", help="Search movies from iTunes search API."
    )
    search_parser.add_argument("--country", help="Country code in double letter format")
    search_parser.add_argument("--term", help="Name of the movie to search")

    args = parser.parse_args()
    if args.command == "extract":
        return extract(args.url, args.thumbnail, args.use_selenium)
    if args.command == "search":
        return search(args.country, args.term)


def extract(url: str, thumbnail: bool, use_selenium: bool) -> None:
    url = clean_url(url)
    domain = extract_domain(url)

    if domain != "tv.apple.com":
        raise ValueError(f"unsupported domain {domain}")

    movie_path = get_movie_path(url)

    artworks = extract_artworks(
        url, thumbnail=thumbnail, movie_path=movie_path, use_selenium=use_selenium
    )

    title, poster_url = extract_artwork(movie_path)
    if poster_url:
        artworks["poster"] = poster_url

    print_artworks(title, artworks)


def search(country: str, term: str) -> None:
    movies_images = get_artworks(country, term, how_many=10)
    print_search_results(movies_images)


if __name__ == "__main__":
    main()

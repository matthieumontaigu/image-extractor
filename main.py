import argparse

from services.apple_tv_service import scrape_apple_tv_image
from services.itunes_service import get_itunes_movies_images, scrape_itunes_image
from utils.print_helpers import print_extract_results, print_search_results
from utils.url_helpers import clean_url, extract_domain, get_movie_path


def main():
    parser = argparse.ArgumentParser(description="Fetch movie posters")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    extract_parser = subparsers.add_parser(
        "extract", help="Get movie poster URL from Apple TV and iTunes"
    )
    extract_parser.add_argument("--url", help="URL of the movie")
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
        return extract(args.url, args.use_selenium)
    if args.command == "search":
        return search(args.country, args.term)


def extract(url, use_selenium):
    url = clean_url(url)
    domain = extract_domain(url)

    if domain != "tv.apple.com":
        raise ValueError(f"unsupported domain {domain}")

    movie_path = get_movie_path(url)
    itunes_image = scrape_itunes_image(movie_path)
    apple_tv_image = scrape_apple_tv_image(url, movie_path, use_selenium)
    print_extract_results(itunes_image, apple_tv_image)


def search(country, term):
    movies_images = get_itunes_movies_images(country, term, how_many=10)
    print_search_results(movies_images)


if __name__ == "__main__":
    main()

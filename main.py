import argparse

from services.apple_tv_service import scrape_apple_tv_image
from services.itunes_service import scrape_itunes_image
from utils.print_helpers import print_results
from utils.url_helpers import clean_url, extract_domain, get_movie_path


def main():
    parser = argparse.ArgumentParser(description="Fetch movie posters.")
    parser.add_argument("--url", help="URL of the movie")
    parser.add_argument(
        "--use-selenium",
        action="store_true",
        help="Authorize the usage of selenium library to extend scrapping capabilities",
    )
    args = parser.parse_args()

    url = clean_url(args.url)
    domain = extract_domain(url)

    if domain != "tv.apple.com":
        raise ValueError(f"unsupported domain {domain}")

    movie_path = get_movie_path(url)
    itunes_image = scrape_itunes_image(movie_path)
    apple_tv_image = scrape_apple_tv_image(url, movie_path, args.use_selenium)
    print_results(itunes_image, apple_tv_image)


if __name__ == "__main__":
    main()

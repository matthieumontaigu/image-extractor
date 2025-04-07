import json
import time

from bs4 import BeautifulSoup
from utils.parsing_helpers import parse_html
from utils.request_helpers import make_get_request
from utils.selenium_helpers import click_button, get_chrome_driver
from utils.url_helpers import get_resized_image_url


def get_thumbnail_url(
    page: BeautifulSoup, movie_path: str, use_selenium: bool
) -> str | None:
    profiles_urls = get_profiles_urls(page)
    if not profiles_urls:
        print("No profiles found for this title.")
        return None

    movies_items = get_movies_items_using_requests(profiles_urls, movie_path)
    if not movies_items and use_selenium:
        movies_items = get_movies_items_using_selenium(profiles_urls, movie_path)

    if not movies_items:
        print("Input movie not found in all profile pages.")
        return None

    movie_item = movies_items[0]
    image_url = get_image_url(movie_item)
    return image_url


def get_movies_items_using_requests(
    profiles_urls: list[str], movie_path: str, request_interval: float = 0.1
) -> list[BeautifulSoup] | None:
    """
    A standard request retrieves only the first five movie items visible on the profile page
    for a given profile URL. This method is limited to the initial set of movies displayed
    without any further interaction or navigation.
    """
    for profile_url in profiles_urls:
        profile_page = make_get_request(profile_url)
        parsed_profile_page = parse_html(profile_page.text)
        movies_items = get_movies_items(parsed_profile_page, movie_path)
        if movies_items:
            return movies_items
        time.sleep(request_interval)
    return None


def get_movies_items_using_selenium(
    profiles_urls: list[str],
    movie_path: str,
    max_clicks: int = 5,
    page_load_timeout: float = 0.5,
) -> list[BeautifulSoup] | None:
    """
    A request using selenium allows to navigate through all the movie items of a given profile URL.
    Click on the arrow 'next' button to load next movie elements until the desired movie_path is found.

    Arguments:
        - max_clicks: define how many times we click on the 'next' button when no new movies are being displayed.
            This is to avoid infinite clicks when no new elements are shown after a click on `next`.
    """
    driver = get_chrome_driver()

    profile_url = profiles_urls[0]
    driver.get(profile_url)

    seen_movies: set[str] = set()
    no_effect_clicks: int = 0
    while no_effect_clicks < max_clicks:
        parsed_profile_page = parse_html(driver.page_source)
        movies_items = get_movies_items(parsed_profile_page, movie_path)
        if movies_items:
            break

        visible_movies = get_movies_names(parsed_profile_page)
        if visible_movies == seen_movies:
            no_effect_clicks += 1
        else:
            no_effect_clicks = 0
            seen_movies = visible_movies

        click_button(
            driver,
            "//button[@class='shelf-grid-nav__arrow shelf-grid-nav__arrow--next']",
        )
        time.sleep(page_load_timeout)

    driver.quit()
    return movies_items


def get_profiles_urls(parsed_page: BeautifulSoup) -> list[str]:
    profiles = parsed_page.find_all("a", class_="profile-lockup")
    if not profiles:
        return []

    profiles_urls = [
        json.loads(profile["data-metrics-click"])["actionUrl"] for profile in profiles
    ]
    return profiles_urls


def get_movies_items(
    parsed_profile_page: BeautifulSoup, movie_path: str
) -> list[BeautifulSoup]:
    return parsed_profile_page.find_all("a", href=movie_path)


def get_movies_names(parsed_profile_page: BeautifulSoup) -> set[str]:
    return set(
        [
            json.loads(div["data-metrics-location"])["name"]
            for div in parsed_profile_page.find_all(
                "div", class_="canvas-lockup", attrs={"data-metrics-location": True}
            )
        ]
    )


def get_title(movie_item: BeautifulSoup) -> str:
    return movie_item["aria-label"]


def get_image_url(movie_item: BeautifulSoup) -> str:
    movie_image = movie_item.div.picture.find_all("source", type="image/jpeg")[0]
    movie_image_url = movie_image["srcset"].split("w, ")[-1].split(" ")[0]
    return get_resized_image_url(movie_image_url, "3840x2160.jpg")

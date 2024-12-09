import json
import time

from utils.parsing_helpers import parse_html
from utils.request_helpers import make_get_request
from utils.selenium_helpers import click_button, get_chrome_driver
from utils.url_helpers import get_resized_image_url


def scrape_apple_tv_image(url, movie_path, use_selenium):
    page = make_get_request(url)
    parsed_page = parse_html(page.text)
    profiles_urls = get_profiles_urls(parsed_page)
    if not profiles_urls:
        print("No profiles found for this title.")
        return

    movies_items = get_movies_items_using_requests(profiles_urls, movie_path)
    if not movies_items and use_selenium:
        movies_items = get_movies_items_using_selenium(profiles_urls, movie_path)

    if not movies_items:
        print("Input movie not found in all profile pages.")
        return

    movie_item = movies_items[0]
    title = get_title(movie_item)
    image_url = get_image_url(movie_item)
    return title, image_url


def get_movies_items_using_requests(profiles_urls, movie_path, request_interval=0.1):
    """
    A standard request returns only load 5 movie items for a given profile URL.
    The first five movies visible on the profile page.
    """
    for profile_url in profiles_urls:
        profile_page = make_get_request(profile_url)
        parsed_profile_page = parse_html(profile_page.text)
        movies_items = get_movies_items(parsed_profile_page, movie_path)
        if movies_items:
            return movies_items
        time.sleep(request_interval)


def get_movies_items_using_selenium(profiles_urls, movie_path, max_clicks=5):
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

    seen_movies, no_effect_clicks = set(), 0
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

        click_button(
            driver,
            "//button[@class='shelf-grid-nav__arrow shelf-grid-nav__arrow--next']",
        )
        # Wait for the dynamically loaded content to appear
        time.sleep(0.5)

    driver.quit()


def get_title(movie_item):
    return movie_item["aria-label"]


def get_image_url(movie_item):
    movie_image = movie_item.div.picture.find_all("source", type="image/jpeg")[0]
    movie_image_url = movie_image["srcset"].split("w, ")[-1].split(" ")[0]
    return get_resized_image_url(movie_image_url, "3840x2160.jpg")


def get_profiles_urls(parsed_page):
    profiles = parsed_page.find_all("a", class_="profile-lockup")
    if not profiles:
        return []

    profiles_urls = [
        json.loads(profile["data-metrics-click"])["actionUrl"] for profile in profiles
    ]
    return profiles_urls


def get_movies_items(parsed_profile_page, movie_path):
    return parsed_profile_page.find_all("a", href=movie_path)


def get_movies_names(parsed_profile_page):
    return set(
        [
            json.loads(div["data-metrics-location"])["name"]
            for div in parsed_profile_page.find_all(
                "div", class_="canvas-lockup", attrs={"data-metrics-location": True}
            )
        ]
    )

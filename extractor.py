import argparse
import json
import re
import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_movie_poster_url(url):
    print(f"\n{url}\n")
    # URLs from Apple TV Mac contains parameters that need to be removed (split ?)
    # URLS from Safari Mac are doubled, take the first one (split \n)
    url = url.split("\n")[0].split("?")[0]
    domain = urlparse(url).netloc
    if domain == "tv.apple.com":
        get_tv_and_itunes_movie_poster_url(url)
    else:
        print("Unknown domain. Please input a correct URL.")


def print_itunes_search_results(country, term, how_many=None):
    itunes_search_results = get_itunes_search_results(country, term)
    if not itunes_search_results:
        return

    how_many = min(how_many, len(itunes_search_results))
    itunes_search_results = (
        itunes_search_results[:how_many] if how_many else itunes_search_results
    )
    for result in itunes_search_results:
        print(f"\n{result['trackName']} ({result['releaseDate']})")
        print(result["artworkUrl100"].replace("100x100bb", "2000x0w"))


def get_itunes_search_results(country, term):
    url = f"https://itunes.apple.com/search?entity=movie&country={country}&term={term}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"{response.status_code} error: {response.text}")
        return
    response_json = response.json()
    if response_json["resultCount"] == 0:
        print("No match found in iTunes.")
        return
    return response_json["results"]


def get_tv_and_itunes_movie_poster_url(url):
    movie_path = get_tv_movie_poster_url(url)
    get_itunes_movie_poster_from_path(movie_path)


def get_tv_movie_poster_url(url, selenium_fallback=True):
    # Extract movie path for future matching
    movie_path = re.search(r"tv.apple.com(.+)$", url).groups()[0]
    movie_page = requests.get(url)
    movie_page_parsed = BeautifulSoup(movie_page.text, "html.parser")
    profiles = movie_page_parsed.find_all("a", class_="profile-lockup")
    if not profiles:
        print("No actors found for this movie.")
        return movie_path

    profiles_urls = [
        json.loads(profile["data-metrics-click"])["actionUrl"] for profile in profiles
    ]

    movies_items = extract_movie_item_from_all_profiles_urls(profiles_urls, movie_path)
    if not movies_items:
        if not selenium_fallback:
            print("Input movie not found in all profile pages.")
            return movie_path
        movies_items = extract_movie_item_from_profile_url(profiles_urls[0], movie_path)
        if not movies_items:
            print("Input movie not found in all profile pages.")
            return movie_path

    movie_item = movies_items[0]
    print(movie_item["aria-label"])
    movie_image = movie_item.div.picture.find_all("source", type="image/jpeg")[0]
    movie_image_url = movie_image["srcset"].split("w, ")[-1].split(" ")[0]
    movie_image_url = re.sub(r"[\d]+x[\d]+\.jpg$", "3840x2160.jpg", movie_image_url)
    print(movie_image_url)
    return movie_path


def extract_movie_item_from_profile_url(profile_url, movie_path):
    # Set up Chrome options to run headless (= without opening a browser window)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize a Chrome webdriver
    driver = webdriver.Chrome(options=chrome_options)
    # driver.implicitly_wait(0.5)
    driver.set_window_size(2560, 1080)

    # Open the webpage
    driver.get(profile_url)

    seen_movies = set()
    counter = 0
    while counter < 5:
        # Retrieve the HTML of the entire page
        page_source = driver.page_source
        movie_page_parsed = BeautifulSoup(page_source, "html.parser")
        movies_items = movie_page_parsed.find_all("a", href=movie_path)
        if movies_items:
            break
        seen_movies, counter = are_there_new_movies(
            movie_page_parsed, seen_movies, counter
        )
        button = driver.find_element(
            By.XPATH,
            "//button[@class='shelf-grid-nav__arrow shelf-grid-nav__arrow--next']",
        )
        button.click()
        # NOT WORKING
        # Wait for the dynamically loaded content to appear (adjust timeout as necessary, here 10 seconds)
        # wait = WebDriverWait(driver, timeout=30, poll_frequency=1)
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='shelf-grid-nav__arrow shelf-grid-nav__arrow--next']")))
        time.sleep(0.5)

    driver.quit()
    return movies_items


def are_there_new_movies(movie_page_parsed, seen_movies, counter):
    are_new_movies = False
    retrieved_movies = set(
        [
            json.loads(div["data-metrics-location"])["name"]
            for div in movie_page_parsed.find_all(
                "div", class_="canvas-lockup", attrs={"data-metrics-location": True}
            )
        ]
    )
    if retrieved_movies == seen_movies:
        counter += 1
    else:
        counter = 0
    return retrieved_movies, counter


def extract_movie_item_from_all_profiles_urls(profiles_urls, movie_path):
    for profile_url in profiles_urls:
        profile_page = requests.get(profile_url)
        profile_page_parsed = BeautifulSoup(profile_page.text, "html.parser")
        movies_items = profile_page_parsed.find_all("a", href=movie_path)
        if movies_items:
            return movies_items
        time.sleep(0.1)


def get_itunes_movie_poster_from_path(movie_path):
    movie_path_parts = movie_path.split("/")
    country = movie_path_parts[1]
    term = movie_path_parts[3]
    print_itunes_search_results(country, term, how_many=1)


def __get_tv_movie_poster_url(url):
    """
    Load Apple TV movie poster when it is the main image of the movie page.
    Discontinued since movie posters are now stored in thumbnails, need to use profiles.
    """
    movie_path = re.search(r"tv.apple.com(.+)$", url).groups()[0]
    movie_page = requests.get(url)
    movie_page_parsed = BeautifulSoup(movie_page.text, "html.parser")
    image_divs = movie_page_parsed.find_all(
        "div", class_="preview-product-header__image"
    )
    if not image_divs:
        print("No main image found for this movie.")
        return
    movie_title_ps = movie_page_parsed.find_all(
        "p", class_="preview-product-header__title typ-headline-emph"
    )
    movie_title = movie_title_ps[0].text
    print(movie_title)
    movie_image = image_divs[0].picture.find_all("source", type="image/jpeg")[0]
    movie_image_url = movie_image["srcset"].split("w, ")[-1].split(" ")[0]
    movie_image_url = re.sub(r"[\d]+x[\d]+\.jpg$", "3840x2160.jpg", movie_image_url)
    print(movie_image_url)
    return


def __get_itunes_movie_poster_url(url):
    """
    Load iTunes movie poster when we know the iTunes movie URL.
    Discontinued since iOS 17.2, December 22nd, 2023. iTunes store has been removed.
    """
    movie_name_search = re.search(r"/([\w\-\%]+)/id", url)
    if not movie_name_search:
        print("No movie name found in URL.")
        return

    movie_name = movie_name_search.groups()[0]
    country = re.search(r"itunes\.apple\.com/([a-z]+)/", url).groups()[0].upper()
    itunes_search_response = requests.get(
        f"https://itunes.apple.com/search?entity=movie&country={country}&term={movie_name}"
    ).json()
    itunes_search_results = itunes_search_response["results"]
    movie_poster_url = None
    for itunes_item in itunes_search_results:
        if url in itunes_item["trackViewUrl"]:
            print(itunes_item["trackName"])
            movie_poster_url = itunes_item["artworkUrl100"]
            break
    if movie_poster_url is None:
        print("No movie found in iTunes search.")
        return

    movie_poster_url = re.sub(r"[\w]+x[\w]+\.jpg$", "2000x0w.jpg", movie_poster_url)
    print(movie_poster_url)
    return


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--url")
    args = argument_parser.parse_args()
    get_movie_poster_url(args.url)

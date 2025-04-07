import re
from urllib.parse import urlparse


def clean_url(url: str) -> str:
    """
    URLs from Apple TV Mac contains parameters that need to be removed (split ?)
    URLS from Safari macOS are doubled, take the first one (split \n)
    """
    url = url.split("\n")[0].split("?")[0]
    return url


def extract_domain(url: str) -> str:
    return urlparse(url).netloc


def get_movie_path(url: str) -> str | None:
    match = re.search(r"tv.apple.com(.+)$", url)
    return match.groups()[0] if match else None


def get_resized_image_url(url: str, size: str) -> str:
    """Example: size = 3840x2160.jpg"""
    return re.sub(r"[\w]+x[\w]+\.jpg$", size, url)

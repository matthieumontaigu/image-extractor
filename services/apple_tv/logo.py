import re

from bs4 import BeautifulSoup
from services.apple_tv.utils import get_image_url


def get_logo_url(page: BeautifulSoup) -> str | None:
    pattern = re.compile(r"^picture")
    pictures = page.find_all("picture", class_=pattern)

    if not pictures:
        return None

    return get_image_url(pictures[0], "2400x900", "png")

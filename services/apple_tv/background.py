from bs4 import BeautifulSoup
from services.apple_tv.utils import get_image_url


def get_background_url(page: BeautifulSoup) -> str | None:
    pictures = page.find_all("picture", class_="svelte-10tj07c")

    if not pictures:
        return None

    return get_image_url(pictures[0], "4320x3240", "jpg")

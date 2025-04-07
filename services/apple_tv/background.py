from bs4 import BeautifulSoup
from services.apple_tv.utils import get_image_url


def get_background_url(page: BeautifulSoup) -> str | None:
    pictures = page.find_all("picture")
    background_picture = None
    for picture in pictures:
        img = picture.find("img", class_="product-header__image-bg")
        if img:
            background_picture = picture
            break

    if not background_picture:
        return None

    return get_image_url(background_picture, "4320x3240", "jpg")

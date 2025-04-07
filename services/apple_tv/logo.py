from bs4 import BeautifulSoup
from services.apple_tv.utils import get_image_url


def get_logo_url(page: BeautifulSoup) -> str | None:
    pictures = page.find_all("picture")
    logo_picture = None
    for picture in pictures:
        img = picture.find("img", class_="product-header__image-logo__image")
        if img:
            logo_picture = picture
            break

    if not logo_picture:
        return None

    return get_image_url(logo_picture, "2400x900", "png")

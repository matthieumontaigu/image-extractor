from bs4 import BeautifulSoup
from utils.url_helpers import get_resized_image_url


def get_image_url(picture: BeautifulSoup, size: str, extension: str) -> str | None:
    srcsets = [source.get("srcset") for source in picture.find_all("source")]
    srcset = None
    file_extension = f".{extension} "
    for srcset in srcsets:
        if file_extension in srcset:
            break
    if not srcset:
        return None

    image_url = srcset.split(", ")[0].split(" ")[0]
    target_size = f"{size}.{extension}"
    return get_resized_image_url(image_url, target_size)

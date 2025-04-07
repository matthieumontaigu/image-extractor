from services.apple_tv.background import get_background_url
from services.apple_tv.logo import get_logo_url
from services.apple_tv.thumbnail import get_thumbnail_url
from utils.parsing_helpers import parse_html
from utils.request_helpers import make_get_request


def extract_artworks(
    url: str,
    logo: bool = True,
    background: bool = True,
    thumbnail: bool = True,
    movie_path: str = "",
    use_selenium: bool = False,
) -> dict[str, str]:
    """
    Extracts artwork URLs (logo, background, and thumbnail) from a given webpage.

    Args:
        url (str): The URL of the webpage to extract artworks from.
        movie_path (str): The path to the movie file, used for generating the thumbnail.
        logo (bool, optional): Whether to extract the logo URL. Defaults to True.
        background (bool, optional): Whether to extract the background URL. Defaults to True.
        thumbnail (bool, optional): Whether to extract the thumbnail URL. Defaults to True.
        use_selenium (bool, optional): Whether to use Selenium for thumbnail extraction. Defaults to False.

    Returns:
        dict[str, str]: A dictionary containing the extracted artwork URLs.
                        Keys are "logo", "background", and "thumbnail", and values are the corresponding URLs.
                        Only includes keys for which extraction was enabled and successful.
    """
    page = make_get_request(url)
    parsed_page = parse_html(page.text)

    extractors = {
        "logo": lambda: get_logo_url(parsed_page),
        "background": lambda: get_background_url(parsed_page),
        "thumbnail": lambda: get_thumbnail_url(parsed_page, movie_path, use_selenium),
    }
    images_types = {
        "logo": logo,
        "background": background,
        "thumbnail": thumbnail,
    }

    artworks: dict[str, str] = {}
    for image_type, extract in images_types.items():
        if not extract:
            continue
        artwork_url = extractors[image_type]()
        if artwork_url is not None:
            artworks[image_type] = artwork_url

    return artworks

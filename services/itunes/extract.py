from services.itunes.search import search_movies


def extract_artwork(movie_path: str) -> tuple[str, str] | None:
    movie_path_parts = movie_path.split("/")
    country = movie_path_parts[1]
    term = movie_path_parts[3]
    movies_artworks = get_artworks(country, term, how_many=1)
    if not movies_artworks:
        return None
    return movies_artworks[0]


def get_artworks(country: str, term: str, how_many: int) -> list[tuple[str, str]]:
    search_results = search_movies(country, term)
    if not search_results:
        return []

    movies_artworks = []
    for rank, itunes_result in enumerate(search_results):
        if rank + 1 > how_many:
            break
        title = get_title(itunes_result)
        image_url = get_artwork_url(itunes_result)
        movies_artworks.append((title, image_url))
    return movies_artworks


def get_title(itunes_result: dict) -> str:
    # Format the title to include the release date
    return f"{itunes_result['trackName']} ({itunes_result['releaseDate']})"


def get_artwork_url(itunes_result: dict) -> str:
    # 2000x0w is the largest image size available
    return itunes_result["artworkUrl100"].replace("100x100bb", "2000x0w")

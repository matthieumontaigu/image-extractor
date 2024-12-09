from utils.request_helpers import make_get_request


def scrape_itunes_image(movie_path):
    movie_path_parts = movie_path.split("/")
    country = movie_path_parts[1]
    term = movie_path_parts[3]
    movies_images = get_itunes_movies_images(country, term, how_many=1)
    if not movies_images:
        return
    return movies_images[0]


def get_itunes_movies_images(country, term, how_many):
    search_results = search_itunes_movies(country, term)
    if not search_results:
        return []

    movies_images = []
    for rank, itunes_result in enumerate(search_results):
        if rank + 1 > how_many:
            break
        title = get_title(itunes_result)
        image_url = get_image_url(itunes_result)
        movies_images.append((title, image_url))
    return movies_images


def search_itunes_movies(country, term):
    url = f"https://itunes.apple.com/search?entity=movie&country={country}&term={term}"
    response = make_get_request(url)
    response_json = response.json()
    if response_json["resultCount"] == 0:
        print("No match found in iTunes.")
        return
    return response_json["results"]


def get_title(itunes_result):
    return f"{itunes_result['trackName']} ({itunes_result['releaseDate']})"


def get_image_url(itunes_result):
    return itunes_result["artworkUrl100"].replace("100x100bb", "2000x0w")

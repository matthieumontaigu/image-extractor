from utils.request_helpers import make_get_request


def search_movies(country: str, term: str) -> list[dict] | None:
    url = f"https://itunes.apple.com/search?entity=movie&country={country}&term={term}"
    response = make_get_request(url)
    response_json = response.json()
    if response_json["resultCount"] == 0:
        print("No match found in iTunes.")
        return None
    return response_json["results"]

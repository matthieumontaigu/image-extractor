import requests
from requests import Response


def make_get_request(url: str) -> Response:
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error {response.status_code}: {response.text}")
    return response

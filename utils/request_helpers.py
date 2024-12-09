import requests


def make_get_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Error {response.status_code}: {response.text}")
    return response

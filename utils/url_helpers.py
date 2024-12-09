import re
from urllib.parse import urlparse


def clean_url(url):
    url = url.split("\n")[0].split("?")[0]
    return url


def extract_domain(url):
    return urlparse(url).netloc

from bs4 import BeautifulSoup


def parse_html(html):
    return BeautifulSoup(html, "html.parser")

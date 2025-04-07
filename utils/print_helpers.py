def print_artworks(title: str, artworks: dict[str, str]) -> None:
    artworks_types = ["poster", "background", "logo", "thumbnail"]
    print("\n")
    print(title)
    print("\n")
    for artwork_type in artworks_types:
        artwork_url = artworks.get(artwork_type)
        if artwork_url is None:
            continue
        print(artwork_type.upper())
        print(artwork_url)
        print("\n")


def print_search_results(movies_images: list[tuple[str, str]]) -> None:
    print("\n")
    for title, image_url in movies_images:
        print(title)
        print(image_url)
        print("\n")

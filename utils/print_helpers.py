def print_extract_results(itunes_image, apple_tv_image):
    if not itunes_image and not apple_tv_image:
        return

    print("\n")
    if itunes_image is not None:
        title, image_url = itunes_image
        print(title)
        print(image_url)
        print("\n")

    if apple_tv_image is not None:
        title, image_url = apple_tv_image
        print(title)
        print(image_url)
        print("\n")


def print_search_results(movies_images):
    for title, image_url in movies_images:
        print(title)
        print(image_url)
        print("\n")

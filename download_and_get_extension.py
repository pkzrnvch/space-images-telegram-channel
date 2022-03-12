from pathlib import Path
from urllib.parse import urlsplit

import requests

def download_image(image_url, file_path, payload=None):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(image_url, params=payload)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def get_extension(image_url):
    split_url = urlsplit(image_url)
    url_path = Path(split_url.path)
    extension = url_path.suffix
    return extension
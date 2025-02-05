import os
import requests
import re
from tqdm import tqdm
from urllib.parse import quote, unquote

from src.utils import save_image_to_file


def get_image_extension(img_url, response):
    if img_url.lower().endswith(".png"):
        return ".png"
    elif img_url.lower().endswith(".jpg") or img_url.lower().endswith(".jpeg"):
        return ".jpg"
    else:
        content_type = response.headers.get("content-type", "")
        if "png" in content_type.lower():
            return ".png"
        else:
            return ".jpg"


def google_image_scraper(search_query, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    image_pattern = r'https?://[^"\'<>\s]+?(?:\.jpg|\.jpeg|\.png)(?:[^"\'<>\s])*'
    downloaded = 0
    all_image_urls = set()

    for page in range(2):
        encoded_query = quote(search_query)
        start_index = page * 20
        url = f"https://www.google.com/search?q={encoded_query}&tbm=isch&start={start_index}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            image_urls = set(re.findall(image_pattern, response.text, re.IGNORECASE))
            image_urls = [unquote(url) for url in image_urls]
            all_image_urls.update(image_urls)
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch image links: {str(e)}") from e

    num_images = len(all_image_urls)
    print(f"Found {num_images} image links for query: {search_query}")

    for img_url in tqdm(
        all_image_urls, desc="Downloading Images", unit="image", total=num_images
    ):
        try:
            if not img_url.startswith("http"):
                continue

            response = requests.get(img_url, headers=headers, timeout=10)
            if response.status_code == 200:
                ext = get_image_extension(img_url, response)
                image_path = os.path.join(output_dir, f"{downloaded+1}{ext}")
                save_image_to_file(response.content, image_path)
                downloaded += 1
            # else:
            #     print(
            #         f"Failed to download image from {img_url}: {response.status_code}"
            #     )
        except Exception as e:
            print(f"Failed to download image from {img_url}")

    print(f"Successfully downloaded {downloaded} images")
    return downloaded

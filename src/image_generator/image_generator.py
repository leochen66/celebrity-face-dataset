import os
import tempfile
import pandas as pd

from src.image_generator.google_image_scraper import google_image_scraper
from src.image_generator.image_face_processor import ImageFaceProcessor


def image_generator(category, number_of_images, lists_dir, images_dir):
    list_path = os.path.join(lists_dir, f"{category}.xlsx")
    names = list(pd.read_excel(list_path)["name"])

    for name in names:
        with tempfile.TemporaryDirectory() as image_tmp_dir:
            google_image_scraper(name, image_tmp_dir)

            processor = ImageFaceProcessor()
            processor.process_images(image_tmp_dir, f"{images_dir}/{category}/{name}")

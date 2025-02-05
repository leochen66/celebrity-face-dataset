import os
import pytest

from src.image_generator.google_image_scraper import google_image_scraper

TEST_OUTPUT_DIR = "test_outputs"


@pytest.fixture
def test_output_dir():
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    return TEST_OUTPUT_DIR


def test_google_image_scraper(test_output_dir):
    search_query = "face images"
    output_path = os.path.join(test_output_dir, search_query)
    google_image_scraper(search_query, output_path)

    downloaded_files = os.listdir(output_path)
    assert len(downloaded_files) > 0

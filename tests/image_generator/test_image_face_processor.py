import os
import pytest
from datetime import datetime

from src.image_generator.image_face_processor import ImageFaceProcessor


def test_image_face_processor():
    # Create processor instance
    processor = ImageFaceProcessor(max_images=10)

    # Setup directories
    test_input_dir = "test_outputs"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_output_base = f"test_outputs/processed_outputs_{timestamp}"

    # Get all sub-directories
    person_dirs = [
        d
        for d in os.listdir(test_input_dir)
        if os.path.isdir(os.path.join(test_input_dir, d))
    ]

    for person_dir in person_dirs:
        input_dir = os.path.join(test_input_dir, person_dir)
        output_dir = os.path.join(test_output_base, person_dir)

        # Process images
        processor.process_images(input_dir, output_dir)

        # Basic verification
        assert os.path.exists(
            output_dir
        ), f"Output directory for {person_dir} was not created"
        processed_images = [
            f
            for f in os.listdir(output_dir)
            if f.endswith((".jpg", ".jpeg", ".png", ".bmp"))
        ]
        assert len(processed_images) > 0, f"No images were processed for {person_dir}"

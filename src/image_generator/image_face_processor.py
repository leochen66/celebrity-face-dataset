import os
import cv2
import dlib
import numpy as np
from tqdm import tqdm


class ImageFaceProcessor:
    def __init__(
        self,
        min_face_size_ratio=0.2,
        sharpness_threshold=100,
        max_images=50,
        max_image_side=400,
        padding_ratio=0.5,
    ):
        self.detector = dlib.get_frontal_face_detector()
        self.min_face_size_ratio = min_face_size_ratio
        self.sharpness_threshold = sharpness_threshold
        self.max_images = max_images
        self.max_image_side = max_image_side
        self.padding_ratio = padding_ratio

    def face_detector(self, image_path):
        try:
            img = cv2.imread(image_path)
            if img is None:
                return False

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector(gray, 1)

            if len(faces) != 1:
                return False

            face = faces[0]
            face_width = face.right() - face.left()
            face_height = face.bottom() - face.top()

            min_face_size = min(img.shape[0], img.shape[1]) * self.min_face_size_ratio
            if face_width < min_face_size or face_height < min_face_size:
                return False

            face_region = gray[face.top() : face.bottom(), face.left() : face.right()]
            if face_region.size == 0:
                return False

            laplacian_var = cv2.Laplacian(face_region, cv2.CV_64F).var()
            if laplacian_var <= self.sharpness_threshold:
                return False

            # Calculate padded region
            padding_x = int(face_width * self.padding_ratio)
            padding_y = int(face_height * self.padding_ratio)

            left = max(0, face.left() - padding_x)
            right = min(img.shape[1], face.right() + padding_x)
            top = max(0, face.top() - padding_y)
            bottom = min(img.shape[0], face.bottom() + padding_y)

            face_image = img[top:bottom, left:right]
            return True, face_image

        except Exception as e:
            raise RuntimeError(f"Face detection error for {image_path}: {str(e)}")

    def resize(self, image):
        h, w = image.shape[:2]
        scale = self.max_image_side / max(h, w)

        if scale >= 1:
            return image

        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    def process_images(self, input_dir, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        valid_face_images = []

        image_files = [
            f
            for f in os.listdir(input_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
        ]

        # Process each image
        for filename in tqdm(image_files, desc="Processing Images"):
            image_path = os.path.join(input_dir, filename)

            result = self.face_detector(image_path)
            if result:
                _, face_image = result
                valid_face_images.append(face_image)

        print(f"Total valid face images found: {len(valid_face_images)}")

        # Sort images by sharpness
        valid_face_images.sort(
            key=lambda x: cv2.Laplacian(
                cv2.cvtColor(x, cv2.COLOR_BGR2GRAY), cv2.CV_64F
            ).var(),
            reverse=True,
        )

        # Select top images and resize
        for i, face_image in enumerate(valid_face_images[: self.max_images]):
            resized_image = self.resize(face_image)

            output_path = os.path.join(output_dir, f"{i+1}.jpg")
            cv2.imwrite(output_path, resized_image)

import os
import pandas as pd


def df_to_excel(df, output_path):
    parent_dir = os.path.dirname(output_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    df.to_excel(output_path, index=False)


def save_image_to_file(image, image_path):
    with open(image_path, "wb") as f:
        f.write(image)

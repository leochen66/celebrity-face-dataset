import pandas as pd

from src.utils import df_to_excel
from src.list_generator.fetch_names import fetch_names


def list_generator(category, number_of_persons, lists_dir):
    names = fetch_names(category, number_of_persons)
    df = pd.DataFrame({"name": names})

    list_path = f"{lists_dir}/{category}.xlsx"
    df_to_excel(df, list_path)

    print(f"List successfully generate in path: {list_path}")

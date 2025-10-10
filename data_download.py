import pandas as pd
import numpy as np
import kagglehub
import chardet
import os
import zipfile

def data_download():
    dataset_path = kagglehub.dataset_download("arashnic/book-recommendation-dataset")

    for file in os.listdir(dataset_path):
        full_path = os.path.join(dataset_path, file)
        if zipfile.is_zipfile(full_path):
            with zipfile.ZipFile(full_path, 'r') as zf:
                zf.extractall(dataset_path)

    books_path = os.path.join(dataset_path, "Books.csv")
    ratings_path = os.path.join(dataset_path, "Ratings.csv")

    df_books = pd.read_csv(books_path, encoding='utf-8')
    df_ratings = pd.read_csv(ratings_path, encoding='utf-8')
    return df_books, df_ratings

def nan_rows(df):
    rows_with_nan = df[df.isna().any(axis=1)]
    return rows_with_nan


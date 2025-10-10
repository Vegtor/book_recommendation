import pandas as pd
import numpy as np
import kagglehub
import chardet
import os
import zipfile
import re

from pandas.core.interchange.dataframe_protocol import DataFrame


def data_download(file_path):
    dataset_path = kagglehub.dataset_download("arashnic/book-recommendation-dataset")

    for file in os.listdir(dataset_path):
        full_path = os.path.join(dataset_path, file)
        if zipfile.is_zipfile(full_path):
            with zipfile.ZipFile(full_path, 'r') as zf:
                zf.extractall(dataset_path)

    books_path = os.path.join(dataset_path, "Books.csv")
    ratings_path = os.path.join(dataset_path, "Ratings.csv")

    df_books = pd.read_csv(books_path, encoding='utf-8', sep=",")
    df_ratings = pd.read_csv(ratings_path, encoding='utf-8', sep=",")

    df_books.to_csv(file_path + "/books.csv" , index=False)
    df_ratings.to_csv(file_path + "/ratings.csv" , index=False)

def check_isbn(df):
    pattern = re.compile(r'^[0-9Xx]+$')
    invalid_mask = ~df['ISBN'].astype(str).str.match(pattern)
    invalid_isbns = df.loc[invalid_mask, 'ISBN'].unique()
    return pd.Series(invalid_isbns)

def delete_missing_books(df_books, df_ratings):
    valid_isbns = set(df_books['ISBN'])
    cleaned_ratings = df_ratings[df_ratings['ISBN'].isin(valid_isbns)].copy()
    cleaned_ratings.reset_index(drop=True, inplace=True)
    return cleaned_ratings

def clean_isbn(df):
    cleaned = df['ISBN'].str.replace(r'ISBN:|ISBN|[-"\t/\.=_*?\\+]', '', regex=True)
    cleaned = cleaned.str.split("<").str[0].str.split(">").str[0].str.split("(").str[0].str.split(" ").str[0]
    return cleaned

def nan_rows(df):
    rows_with_nan = df[df.isna().any(axis=1)]
    return rows_with_nan


import pandas as pd
import numpy as np
import os
import kagglehub
from kagglehub import KaggleDatasetAdapter



def data_download():
    df_books = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "arashnic/book-recommendation-dataset",
        "Books.csv",
    )
    df_ratings = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "arashnic/book-recommendation-dataset",
        "Ratings.csv",
    )
    return df_books, df_ratings

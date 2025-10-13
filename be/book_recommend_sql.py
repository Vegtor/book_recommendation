import pandas as pd
from sqlalchemy import create_engine, text
import os

db_user = os.getenv("POSTGRES_USER", "book_owner")
db_pass = os.getenv("POSTGRES_PASSWORD", "book_pass")
db_name = os.getenv("POSTGRES_DB", "book_db")
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL)

def recomendation_sql_v3(book_name, author=None, book_publisher=None, year_pb=None, isbn=None):
    query = text("""SELECT * FROM find_book_by_info_id(:book_name, :search_author, :search_publisher, :search_year, :search_isbn, 0.3)""")

    with engine.connect() as conn:
        book_id_df = pd.read_sql(
            query,
            conn,
            params={
                "book_name": book_name,
                "search_author": author,
                "search_publisher": book_publisher,
                "search_year": year_pb,
                "search_isbn": isbn
            }
        )

    if book_id_df.empty or book_id_df is None:
        raise Exception(-1, "No book found for this search query")
    book_id = int(book_id_df.iloc[0]['book_id'])

    query_searched_book = text("""SELECT b."Book-Title"  AS book_name,
                                         b."Book-Author" AS book_author,
                                         b."Publisher"   AS publisher,
                                         b."Year-Of-Publication" AS year, 
                                         b."ISBN" AS isbn, 
                                         b."Image-URL-M" AS url_m
                                  FROM books b
                                  WHERE b."id" = :book_id""")
    with engine.connect() as conn:
        searched_book = pd.read_sql(query_searched_book, conn, params={"book_id": book_id})

    query_avg = text("""SELECT user_id, book_id, avg_rating FROM get_avg_ratings_for_books_of_readers_id(:book_id)""")
    with engine.connect() as conn:
        df_corr = pd.read_sql(query_avg, conn, params={"book_id": book_id})
    if df_corr.empty or df_corr is None:
        return searched_book, None
    df_corr = df_corr.pivot(index='user_id', columns='book_id', values='avg_rating')

    dataset_of_other_books = df_corr.copy(deep=False)
    dataset_of_other_books.drop(book_id, axis=1, inplace=True)
    books_ids = dataset_of_other_books.columns.tolist()

    avg_rating = dataset_of_other_books.mean().round(2)

    correlations = dataset_of_other_books.corrwith(df_corr[book_id])
    correlation_df = pd.DataFrame({
            'book': correlations.index.values,
            'corr': correlations.values,
            'avg_rating': avg_rating.values
        })

    result_list = correlation_df.sort_values('corr', ascending=False)

    query_all_info = text("""SELECT * FROM get_all_info_id(:book_id, 8)""")
    with engine.connect() as conn:
        df_all_info = pd.read_sql(query_all_info, conn, params={"book_id": book_id})

    result = result_list.merge(df_all_info, left_on='book', right_on='book_id', how='left')
    result.drop(columns=['book'], inplace=True)
    return searched_book, result


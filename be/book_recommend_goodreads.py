import pandas as pd
from sqlalchemy import text
from database_manager import DatabaseSingleton

def recommendation_sql_v2(book_name, author=None, year_pb=None, isbn=None):
    db = DatabaseSingleton()
    engine = db.get_engine(1)

    query = text("""SELECT * FROM find_book_by_info_id(:book_name, :search_author, :search_year, :search_isbn, 0.3)""")

    with engine.connect() as conn:
        book_id_df = pd.read_sql(
            query,
            conn,
            params={
                "book_name": book_name,
                "search_author": author,
                "search_year": year_pb,
                "search_isbn": isbn
            }
        )

    if book_id_df.empty or book_id_df is None:
        raise Exception(-1, "No book found for this search query")
    book_id = int(book_id_df.iloc[0]['book_id'])

    query_searched_book = text("""SELECT * FROM get_searched_book_info_id(:book_id)""")
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

    avg_rating = dataset_of_other_books.mean().round(2)

    correlations = dataset_of_other_books.corrwith(df_corr[book_id])
    correlation_df = pd.DataFrame({
            'book_id': correlations.index.values,
            'corr': correlations.values,
            'avg_rating': avg_rating.values
        })

    result_list = correlation_df.sort_values('corr', ascending=False)

    query_all_info = text("""SELECT * FROM get_all_info_id(:book_id, 8)""")
    with engine.connect() as conn:
        df_all_info = pd.read_sql(query_all_info, conn, params={"book_id": book_id})

    result = result_list.merge(df_all_info, left_on='book_id', right_on='book_id', how='left')
    return searched_book, result

def recommendation_sql_v2_1(book_name, author=None, year_pb=None, isbn=None):
    db = DatabaseSingleton()
    engine = db.get_engine(1)

    query = text("""SELECT * FROM find_book_by_info_id(:book_name, :search_author, :search_year, :search_isbn, 0.3)""")

    with engine.connect() as conn:
        book_id_df = pd.read_sql(
            query,
            conn,
            params={
                "book_name": book_name,
                "search_author": author,
                "search_year": year_pb,
                "search_isbn": isbn
            }
        )
    if book_id_df.empty or book_id_df is None:
        raise Exception(-1, "No book found for this search query")
    book_id = int(book_id_df.iloc[0]['book_id'])

    query_searched_book = text("""SELECT * FROM get_searched_book_info_id(:book_id)""")
    with engine.connect() as conn:
        searched_book = pd.read_sql(query_searched_book, conn, params={"book_id": book_id})

    query_all_info = text("""SELECT * FROM get_hybrid_recommendations_all_info(:book_id, 0.5, 0.3, 0.2)""")
    with engine.connect() as conn:
        df_all_info = pd.read_sql(query_all_info, conn, params={"book_id": book_id})
    return searched_book, df_all_info

